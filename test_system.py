import unittest
from app import app
from auth import (
    init_auth_db, register_user, login_user, update_user_profile,
    update_user_avatar, save_valuation, get_saved_valuations, delete_saved_valuation
)
from model_handler import predict_house_price
from bengaluru_data import get_location_infra

class TestBengaluruSystem(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        init_auth_db()

    def test_auth_flow(self):
        login_status, login_res = login_user("demo@bengaluru.com", "password123")
        self.assertTrue(login_status)
        self.assertEqual(login_res["email"], "demo@bengaluru.com")

    def test_chatbot_api(self):
        # Query chatbot endpoint
        res = self.app.post('/api/chatbot', json={'message': 'What is the price in Whitefield?'})
        data = res.get_json()
        self.assertIn('reply', data)
        self.assertIn('Whitefield', data['reply'])
        print("\nChatbot Price Query Reply Sample:\n", data['reply'].encode('ascii', 'ignore').decode('ascii')[:150])

        res2 = self.app.post('/api/chatbot', json={'message': 'Hospitals near Kengeri'})
        data2 = res2.get_json()
        self.assertIn('Hospitals', data2['reply'])

    def test_avatar_update(self):
        success, msg = update_user_avatar(1, "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==")
        self.assertTrue(success)

    def test_saved_valuations_crud(self):
        success, val_id = save_valuation(1, "Whitefield", 1400, 3, 2, "₹ 85.50 Lakhs", "$103,000 USD")
        self.assertTrue(success)
        vals = get_saved_valuations(1)
        self.assertGreater(len(vals), 0)
        del_success = delete_saved_valuation(val_id, 1)
        self.assertTrue(del_success)

    def test_ml_dual_currency_prediction(self):
        pred = predict_house_price("Whitefield", 1400, 3, 2, 2, "Super Built-up Area", "Ready to Move")
        self.assertIn("lakhs", pred)
        self.assertIn("dollars", pred)
        print("\nML Dual Currency Test Result: INR =", pred["formatted_price_inr"].encode('ascii', 'ignore').decode('ascii'), "| USD =", pred["formatted_price_usd"])

if __name__ == '__main__':
    unittest.main()
