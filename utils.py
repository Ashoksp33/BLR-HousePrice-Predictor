import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def calculate_rmse(actual, predicted):
    """Calculate Root Mean Square Error"""
    return float(np.sqrt(mean_squared_error(actual, predicted)))

def calculate_metrics(actual, predicted):
    """Calculate various performance metrics"""
    mse = mean_squared_error(actual, predicted)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    
    # Calculate MAPE (Mean Absolute Percentage Error)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100
    
    # Calculate directional accuracy (correct prediction of price movement direction)
    actual_diff = np.diff(actual.flatten())
    pred_diff = np.diff(predicted.flatten())
    directional_accuracy = np.mean((actual_diff * pred_diff) > 0) * 100
    
    return {
        'rmse': round(float(rmse), 2),
        'mae': round(float(mae), 2),
        'mape': round(float(mape), 2),
        'r2': round(float(r2), 4),
        'dir_accuracy': round(float(directional_accuracy), 2)
    }

def format_large_number(num):
    """Format large numbers with B/M suffix"""
    if num is None or num == 'N/A':
        return 'N/A'
    
    if isinstance(num, str):
        return num
        
    if num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.2f}M"
    else:
        return f"${num:.2f}"
