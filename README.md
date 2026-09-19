# 🏠 BLR-HousePrice-Predictor
### Bengaluru House Price Prediction & Real Estate Intelligence System

An end-to-end Machine Learning web application for predicting Bengaluru house prices, exploring public infrastructure (hospitals, Namma Metro, BMTC bus stops, BLR airport), dual currency valuation (₹ INR & $ USD), and an interactive **Meta AI Real Estate Assistant**.

---

## 🌟 Key Features

- **Trained ML Model**: Linear Regression model trained on 13,000+ Bengaluru house price listings supporting 240+ locations (Whitefield, Kengeri, Indiranagar, Koramangala, Electronic City, Yelahanka, HSR Layout, etc.).
- **Dual Currency Valuation**: Displays prices simultaneously in **Indian Rupees (₹ Lakhs / ₹ Cr)** and **US Dollars ($ USD)** (1 USD = 83 INR).
- **Financial Analytics**: Computes Price per Sq.Ft in ₹ and $, 20-Year Home Loan EMI, and valuation price range.
- **Collapsible Pop & Expand Left Sidebar**: Sidebar menu (`FrontendJoe Sidebar 14`) with dark/light mode toggle switch and cursor hover pop-up animations.
- **Settings & Profile Sub-Modules**: Profile photo uploader (camera overlay trigger), Features & Preferences, Saved Valuations History, and Support FAQ center.
- **Public Places & Infrastructure Explorer**: Comprehensive metadata for Hospitals (distances, contacts, addresses), Namma Metro (lines, gates, operational status), BMTC Bus Stops (stop names, route numbers), and Kempegowda Int'l Airport (BLR) travel times.
- **Meta AI Real Estate Assistant**: Floating WhatsApp-style chatbot widget answering instant questions about location prices, hospitals, metro lines, and investment ROI.

---

## 📁 Repository Structure

```
BLR-HousePrice-Predictor/
├── app.py                 # Flask web server, REST API & chatbot route handlers
├── auth.py                # SQLite authentication, user profiles, and saved valuations DB
├── model_handler.py       # Scikit-learn ML model loader & dual currency math engine
├── bengaluru_data.py      # Infrastructure database (Hospitals, Metro, Bus, Airport, Schools, Tech Parks)
├── model.pkl              # Trained scikit-learn Linear Regression model
├── columns.pkl            # ML feature column definitions
├── columns.json           # Data columns JSON metadata
├── test_system.py         # Automated test suite (5 tests passing)
├── static/
│   ├── css/
│   │   ├── auth.css       # Grey & White sliding login page styles
│   │   └── dashboard.css  # Sidebar layout, dark/light theme CSS custom variables
│   └── js/
│       ├── auth.js        # Auth sliding card logic
│       └── dashboard.js   # Sidebar views, avatar upload, saved valuations & Meta AI chatbot
└── templates/
    ├── auth.html          # Grey & White 2-panel sliding login card
    └── dashboard.html     # Main dashboard with sidebar, sub-panels & Meta AI widget
```

---

## 🚀 Quick Start Guide

### 1. Requirements & Dependencies
Make sure Python 3.9+ is installed. Install requirements:
```bash
pip install flask numpy pandas scikit-learn
```

### 2. Run the Server
Launch `app.py`:
```bash
python app.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

---

## 🔐 Demo Credentials

- **Email**: `demo@bengaluru.com`
- **Password**: `password123`

---

## 📜 License
This project is licensed under the MIT License.
