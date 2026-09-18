from flask import Flask, render_template, request, jsonify
import numpy as np
from datetime import datetime, timedelta
import io
import base64
import matplotlib
matplotlib.use('Agg')  # For server environments
import matplotlib.pyplot as plt
import webbrowser
import threading
import time

from data_handler import get_stock_data, get_stock_info
from model import create_and_train_model, predict_future_prices
from utils import calculate_rmse, calculate_metrics

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input parameters
        stock_symbol = request.form['symbol'].upper().strip()
        start_date = request.form['start_date'].strip()
        end_date = request.form['end_date'].strip()
        predict_days = int(request.form.get('predict_days', 7))
        
        # Validate inputs
        if not stock_symbol or not start_date or not end_date:
            return render_template('error.html', error_message="All fields are required")
        
        # Get stock data
        df, error_message = get_stock_data(stock_symbol, start_date, end_date)
        if error_message:
            return render_template('error.html', error_message=error_message)
        
        # Process data and train model
        model, scaler, x_test, y_test, train_data, test_data = create_and_train_model(df)
        
        # Make predictions on test data
        test_predictions = model.predict(x_test, verbose=0)
        test_predictions = scaler.inverse_transform(test_predictions)
        actual_values = scaler.inverse_transform(y_test.reshape(-1, 1))
        
        # Generate future predictions
        future_predictions, future_dates = predict_future_prices(
            model, scaler, df, end_date, predict_days)
        
        # Calculate metrics
        rmse = calculate_rmse(actual_values, test_predictions)
        metrics = calculate_metrics(actual_values, test_predictions)
        
        # Create visualization
        plot_url = generate_plot(df, test_predictions, future_dates, future_predictions)
        
        # Format prediction data for display
        prediction_data = []
        for i, (date, price) in enumerate(zip(future_dates, future_predictions)):
            prediction_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'price': round(float(price), 2),
                'change': '-' if i == 0 else f"{((price / future_predictions[i-1]) - 1) * 100:+.2f}%"
            })
        
        last_price = float(df['Close'].values.flatten()[-1])
        
        return render_template('result.html', 
                               stock_symbol=stock_symbol,
                               metrics=metrics,
                               plot_url=plot_url,
                               prediction_data=prediction_data,
                               last_price=last_price,
                               rmse=rmse)
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Print full stack trace in console
        error_msg = str(e)
        if '429' in error_msg:
            error_msg = "Too many requests sent to the data provider. Please wait and try again later."
        elif 'empty' in error_msg.lower():
            error_msg = "No data received. Please check the stock symbol and date range."
        return render_template('error.html', error_message=f"An error occurred: {error_msg}")

@app.route('/api/stock_info/<symbol>')
def stock_info_endpoint(symbol):
    """API endpoint to get basic stock information"""
    info = get_stock_info(symbol.upper().strip())
    if 'error' in info:
        return jsonify(info), 404
    return jsonify(info)

def generate_plot(df, test_predictions, future_dates, future_predictions):
    """Generate visualization plot"""
    plt.figure(figsize=(12, 6))
    
    close_prices = df['Close'].values.flatten()
    
    # Plot historical data
    plt.plot(df.index, close_prices, label='Historical Data', color='#1f77b4', linewidth=2)
    
    # Plot test predictions
    test_dates = df.index[-len(test_predictions):]
    plt.plot(test_dates, test_predictions.flatten(), label='Test Predictions', color='#2ca02c', alpha=0.8, linewidth=2)
    
    # Plot future predictions
    plt.plot(future_dates, future_predictions, label='Future Predictions', color='#d62728', linestyle='--', linewidth=2.5, marker='o')
    
    # Add details to plot
    plt.title(f'Stock Price Prediction ({df.index[0].strftime("%Y-%m-%d")} to {future_dates[-1].strftime("%Y-%m-%d")})', fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (USD)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Save plot to base64 string
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png', dpi=120)
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    plt.close()
    
    return plot_url

def open_browser():
    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == '__main__':
    print("Starting Stock Market Price Prediction Server on http://127.0.0.1:5000 ...")
    threading.Thread(target=open_browser, daemon=True).start()
    app.run(host='127.0.0.1', port=5000, debug=False)
