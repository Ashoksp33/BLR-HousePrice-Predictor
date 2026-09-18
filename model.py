import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping
from datetime import datetime, timedelta

def create_sequence_data(data, time_steps=60):
    """Create sequence data for LSTM model"""
    x, y = [], []
    for i in range(time_steps, len(data)):
        x.append(data[i-time_steps:i, 0])
        y.append(data[i, 0])
    return np.array(x), np.array(y)

def create_and_train_model(df):
    """Create and train LSTM model"""
    # Extract close price as 1D array flattened
    close_prices = df['Close'].values.flatten().reshape(-1, 1)
    
    # Scale data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(close_prices)
    
    # Determine training/testing split
    train_size = int(len(scaled_data) * 0.8)
    train_data = scaled_data[:train_size]
    test_data = scaled_data[train_size-60:]  # Include 60 previous days for sequence
    
    # Create sequence data
    time_steps = 60  # 60 days of historical data
    x_train, y_train = create_sequence_data(train_data, time_steps)
    x_test, y_test = create_sequence_data(test_data, time_steps)
    
    # Reshape data for LSTM [samples, time steps, features]
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    # Create LSTM model using modern Keras structure
    model = Sequential([
        Input(shape=(time_steps, 1)),
        LSTM(units=50, return_sequences=True),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=25),
        Dense(units=1)
    ])
    
    # Compile model
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Set up early stopping
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    
    # Train model
    model.fit(
        x_train, y_train,
        epochs=50,
        batch_size=32,
        validation_split=0.2,
        callbacks=[early_stop],
        verbose=0
    )
    
    return model, scaler, x_test, y_test, train_data, test_data

def predict_future_prices(model, scaler, df, last_date_str, days_to_predict):
    """Predict future stock prices"""
    close_prices = df['Close'].values.flatten()
    last_sequence = close_prices[-60:].reshape(-1, 1)
    last_sequence_scaled = scaler.transform(last_sequence)
    
    future_predictions = []
    future_dates = []
    
    current_date = datetime.strptime(last_date_str, '%Y-%m-%d')
    current_sequence = last_sequence_scaled.copy()
    
    for i in range(days_to_predict):
        current_date = add_business_day(current_date)
        future_dates.append(current_date)
        
        x_future = current_sequence.reshape(1, 60, 1)
        next_day_scaled = model.predict(x_future, verbose=0)
        
        next_day_price = float(scaler.inverse_transform(next_day_scaled)[0, 0])
        future_predictions.append(next_day_price)
        
        current_sequence = np.append(current_sequence[1:], next_day_scaled, axis=0)
    
    return future_predictions, future_dates

def add_business_day(date):
    """Add one business day to date, skipping weekends"""
    next_day = date + timedelta(days=1)
    while next_day.weekday() > 4:  # Skip Saturday (5) and Sunday (6)
        next_day += timedelta(days=1)
    return next_day
