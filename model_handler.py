import pickle
import json
import numpy as np
import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
COLUMNS_PKL_PATH = os.path.join(os.path.dirname(__file__), 'columns.pkl')
COLUMNS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'columns.json')

_model = None
_columns = None
_locations = []

USD_EXCHANGE_RATE = 83.0  # 1 USD = 83.0 INR approx

def load_ml_assets():
    global _model, _columns, _locations
    if _model is None or _columns is None:
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, 'rb') as f:
                _model = pickle.load(f)
        if os.path.exists(COLUMNS_PKL_PATH):
            with open(COLUMNS_PKL_PATH, 'rb') as f:
                _columns = list(pickle.load(f))
        elif os.path.exists(COLUMNS_JSON_PATH):
            with open(COLUMNS_JSON_PATH, 'r') as f:
                _columns = json.load(f)['data_columns']
        
        _locations = [str(col).title() for col in _columns[3:]]

def get_locations():
    load_ml_assets()
    return _locations

def predict_house_price(location, sqft, bhk, bath, balcony=1, area_type="Super Built-up Area", ready_status="Ready to Move"):
    """
    Predicts house price using trained ML model.
    Returns dict with INR (₹) and USD ($) price formats, EMI, price/sqft, and price bands.
    """
    load_ml_assets()
    
    loc_input = location.lower().strip()
    
    # Construct feature vector DataFrame
    x_df = pd.DataFrame(np.zeros((1, len(_columns))), columns=_columns)
    x_df.iloc[0, 0] = sqft
    x_df.iloc[0, 1] = bath
    x_df.iloc[0, 2] = bhk
    
    found_idx = -1
    for idx, col_name in enumerate(_columns[3:], start=3):
        if str(col_name).lower().strip() == loc_input:
            found_idx = idx
            break
            
    if found_idx != -1:
        x_df.iloc[0, found_idx] = 1
    
    raw_lakhs = float(_model.predict(x_df)[0])
    
    balcony_factor = 1.0 + (int(balcony) - 1) * 0.02
    area_type_factor = 1.05 if area_type == "Super Built-up Area" else (1.0 if area_type == "Built-up Area" else 0.95)
    
    adjusted_lakhs = max(10.0, raw_lakhs * balcony_factor * area_type_factor)
    
    rupees = float(adjusted_lakhs * 100000)
    crores = float(adjusted_lakhs / 100)
    dollars = float(rupees / USD_EXCHANGE_RATE)
    
    price_per_sqft_inr = float(rupees / max(100, sqft))
    price_per_sqft_usd = float(dollars / max(100, sqft))
    
    # 20-Year Loan EMI @ 8.5% p.a. (80% LTV)
    loan_amount_inr = rupees * 0.8
    monthly_r = 0.085 / 12
    n_months = 240
    emi_inr = (loan_amount_inr * monthly_r * ((1 + monthly_r)**n_months)) / (((1 + monthly_r)**n_months) - 1)
    emi_usd = emi_inr / USD_EXCHANGE_RATE
    
    inr_str = f"₹ {adjusted_lakhs:.2f} Lakhs" if adjusted_lakhs < 100 else f"₹ {crores:.2f} Cr"
    usd_str = f"${dollars:,.0f} USD"
    
    return {
        "lakhs": round(adjusted_lakhs, 2),
        "crores": round(crores, 3),
        "rupees": round(rupees),
        "dollars": round(dollars),
        "formatted_price_inr": inr_str,
        "formatted_price_usd": usd_str,
        "formatted_price_combined": f"{inr_str}  •  {usd_str}",
        "price_per_sqft_inr": round(price_per_sqft_inr, 2),
        "price_per_sqft_usd": round(price_per_sqft_usd, 2),
        "estimated_emi_inr": round(emi_inr),
        "estimated_emi_usd": round(emi_usd),
        "min_price_lakhs": round(adjusted_lakhs * 0.92, 2),
        "max_price_lakhs": round(adjusted_lakhs * 1.08, 2),
        "min_price_usd": round((adjusted_lakhs * 0.92 * 100000) / USD_EXCHANGE_RATE),
        "max_price_usd": round((adjusted_lakhs * 1.08 * 100000) / USD_EXCHANGE_RATE),
        "location": location.title(),
        "sqft": sqft,
        "bhk": bhk,
        "bath": bath,
        "balcony": balcony,
        "area_type": area_type,
        "ready_status": ready_status
    }
