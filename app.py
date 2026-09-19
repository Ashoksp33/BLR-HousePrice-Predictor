from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
import re
from auth import (
    init_auth_db, register_user, login_user, update_user_profile,
    update_user_avatar, save_valuation, get_saved_valuations, delete_saved_valuation
)
from model_handler import get_locations, predict_house_price
from bengaluru_data import get_location_infra

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize SQLite database
init_auth_db()

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth.html')

@app.route('/login')
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('auth.html')

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    email = data.get('email', '')
    password = data.get('password', '')
    
    success, result = login_user(email, password)
    if success:
        session['user'] = result
        return jsonify({"success": True, "user": result})
    else:
        return jsonify({"success": False, "message": result}), 400

@app.route('/api/auth/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    name = data.get('name', '')
    email = data.get('email', '')
    password = data.get('password', '')
    
    success, result = register_user(name, email, password)
    if success:
        session['user'] = result
        return jsonify({"success": True, "user": result})
    else:
        return jsonify({"success": False, "message": result}), 400

@app.route('/api/user/update', methods=['POST'])
def api_user_update():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    role = data.get('role', 'UI/UX Designer & Real Estate Investor').strip()
    
    if not name or not email:
        return jsonify({"success": False, "message": "Name and Email are required."}), 400
        
    user_id = session['user']['id']
    success, msg = update_user_profile(user_id, name, email, role)
    if success:
        session['user']['name'] = name
        session['user']['email'] = email
        session['user']['role'] = role
        session.modified = True
        return jsonify({"success": True, "user": session['user'], "message": msg})
    return jsonify({"success": False, "message": msg}), 400

@app.route('/api/user/avatar', methods=['POST'])
def api_user_avatar():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    data = request.get_json() or {}
    avatar_data = data.get('avatar', '').strip()
    if not avatar_data:
        return jsonify({"success": False, "message": "Avatar image data required"}), 400
        
    user_id = session['user']['id']
    success, msg = update_user_avatar(user_id, avatar_data)
    if success:
        session['user']['avatar'] = avatar_data
        session.modified = True
        return jsonify({"success": True, "avatar": avatar_data, "message": msg})
    return jsonify({"success": False, "message": msg}), 400

@app.route('/api/valuations/save', methods=['POST'])
def api_save_valuation():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    data = request.get_json() or {}
    user_id = session['user']['id']
    
    location = data.get('location', '')
    sqft = data.get('sqft', 0)
    bhk = data.get('bhk', 0)
    bath = data.get('bath', 0)
    price_inr = data.get('price_inr', '')
    price_usd = data.get('price_usd', '')
    
    success, val_id = save_valuation(user_id, location, sqft, bhk, bath, price_inr, price_usd)
    if success:
        return jsonify({"success": True, "id": val_id, "message": "Valuation saved to your history!"})
    return jsonify({"success": False, "message": "Failed to save valuation"}), 500

@app.route('/api/valuations', methods=['GET'])
def api_get_valuations():
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    user_id = session['user']['id']
    vals = get_saved_valuations(user_id)
    return jsonify({"success": True, "valuations": vals})

@app.route('/api/valuations/<int:val_id>', methods=['DELETE'])
def api_delete_valuation(val_id):
    if 'user' not in session:
        return jsonify({"success": False, "message": "Unauthorized"}), 401
        
    user_id = session['user']['id']
    delete_saved_valuation(val_id, user_id)
    return jsonify({"success": True, "message": "Valuation deleted"})

@app.route('/api/auth/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    locations = get_locations()
    return render_template('dashboard.html', user=session['user'], locations=locations)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json() or {}
    
    location = data.get('location', 'Whitefield')
    try:
        sqft = float(data.get('sqft', 1200))
        bhk = int(data.get('bhk', 2))
        bath = int(data.get('bath', 2))
        balcony = int(data.get('balcony', 1))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Invalid numeric input parameters."}), 400
        
    area_type = data.get('area_type', 'Super Built-up Area')
    ready_status = data.get('ready_status', 'Ready to Move')
    
    try:
        res = predict_house_price(location, sqft, bhk, bath, balcony, area_type, ready_status)
        return jsonify({"success": True, "prediction": res})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/location_info/<location_name>')
def api_location_info(location_name):
    infra = get_location_infra(location_name)
    return jsonify(infra)

@app.route('/api/chatbot', methods=['POST'])
def api_chatbot():
    data = request.get_json() or {}
    query = data.get('message', '').strip().lower()
    
    if not query:
        return jsonify({"reply": "Hello! How can I assist you with Bengaluru real estate today?"})
        
    locations_list = get_locations()
    found_loc = None
    
    for loc in locations_list:
        if loc.lower() in query:
            found_loc = loc
            break
            
    if not found_loc:
        # Check common aliases
        if 'whitefield' in query: found_loc = 'Whitefield'
        elif 'kengeri' in query: found_loc = 'Kengeri'
        elif 'koramangala' in query: found_loc = 'Koramangala'
        elif 'indiranagar' in query or 'indira nagar' in query: found_loc = 'Indira Nagar'
        elif 'electronic city' in query or 'ecity' in query: found_loc = 'Electronic City'
        elif 'hsr' in query: found_loc = 'HSR Layout'
        elif 'yelahanka' in query: found_loc = 'Yelahanka'

    # Answer location specific queries
    if found_loc:
        infra = get_location_infra(found_loc)
        pred = predict_house_price(found_loc, 1400, 3, 2)
        
        if 'price' in query or 'cost' in query or 'rate' in query or 'valua' in query:
            reply = f"🏠 **{found_loc} Real Estate Valuation**:\n\nFor a standard 3 BHK (1,400 sqft) property in {found_loc}:\n• **Price**: {pred['formatted_price_inr']} ({pred['formatted_price_usd']})\n• **Price/Sq.Ft**: ₹ {pred['price_per_sqft_inr']:,} / sqft (${pred['price_per_sqft_usd']} USD)\n• **Est. 20-Yr Loan EMI**: ₹ {pred['estimated_emi_inr']:,} / month (${pred['estimated_emi_usd']} USD)\n• **Estimated Price Band**: ₹ {pred['min_price_lakhs']} Lakhs to ₹ {pred['max_price_lakhs']} Lakhs"
        elif 'hospital' in query or 'medical' in query or 'doctor' in query:
            h_list = "\n".join([f"• **{h['name']}** ({h['distance']}) - {h['type']}, Ph: {h['contact']}" for h in infra['hospitals']])
            reply = f"🏥 **Hospitals near {found_loc}**:\n\n{h_list}"
        elif 'metro' in query or 'train' in query or 'station' in query:
            m_list = "\n".join([f"• **{m['station']}** ({m['distance']}) - {m['line']}, Gate: {m['gate']}" for m in infra['metro']])
            reply = f"🚇 **Namma Metro Stations near {found_loc}**:\n\n{m_list}"
        elif 'bus' in query or 'bmtc' in query or 'stop' in query:
            b_list = "\n".join([f"• **{b['name']}** ({b['distance']}) - Routes: {b['routes']}" for b in infra['bus_stops']])
            reply = f"🚌 **BMTC Bus Stops near {found_loc}**:\n\n{b_list}"
        elif 'airport' in query or 'flight' in query or 'blr' in query:
            a = infra['airport']
            reply = f"✈️ **Kempegowda International Airport (BLR) Connectivity from {found_loc}**:\n\n• **Distance**: {a['distance']}\n• **Travel Time**: {a['travel_time']}\n• **Airport Shuttle**: {a['kias_bus']}"
        else:
            h_count = len(infra['hospitals'])
            m_count = len(infra['metro'])
            reply = f"🌟 **{found_loc} Overview**:\n\n• **Estimated 3BHK Price**: {pred['formatted_price_inr']} ({pred['formatted_price_usd']})\n• **Hospitals Nearby**: {h_count} major multi-speciality centers\n• **Metro Station**: {infra['metro'][0]['station']} ({infra['metro'][0]['distance']})\n• **Airport Distance**: {infra['airport']['distance']} ({infra['airport']['travel_time']})"
    
    elif 'hi' in query or 'hello' in query or 'hey' in query:
        reply = "👋 Hi there! I'm Meta AI, your Bengaluru Real Estate & Location Assistant. You can ask me about:\n\n1. House prices in Whitefield, Kengeri, Koramangala, etc.\n2. Nearest hospitals, metro stations, and BMTC bus routes\n3. Airport connectivity & travel times\n4. Real estate investment guidance"
    elif 'invest' in query or 'best' in query or 'growth' in query:
        reply = "📈 **Bengaluru Investment Guidance**:\n\n• **Top Tech Corridors**: Whitefield, Electronic City, and Outer Ring Road (ORR) offer 8-11% annual capital appreciation.\n• **High Rental Yield**: Koramangala & Indiranagar offer premium 4.2% rental yields.\n• **Metro Advantage**: Kengeri (Purple Line) and Yelahanka (Airport Line extension) offer high appreciation potential."
    else:
        reply = "I'm Meta AI! Ask me about house prices in any Bengaluru location (e.g. *What's the price in Whitefield?*), nearest hospitals, Namma metro lines, or BMTC bus routes!"
        
    return jsonify({"reply": reply})

if __name__ == '__main__':
    print("Starting Bengaluru House Price Prediction Server on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=True)
