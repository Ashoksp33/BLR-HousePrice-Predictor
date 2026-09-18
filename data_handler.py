import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time

def get_stock_info(symbol):
    """Get basic information about a stock"""
    try:
        time.sleep(0.5)
        ticker = yf.Ticker(symbol)
        
        info = {}
        try:
            info = ticker.info
        except Exception:
            for prop in ['shortName', 'sector', 'industry', 'marketCap', 'trailingPE', 'dividendYield', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow']:
                try:
                    info[prop] = getattr(ticker, prop, 'N/A')
                except Exception:
                    info[prop] = 'N/A'
            
        if not info or len(info) < 3:
            hist = ticker.history(period="1d")
            if hist is None or hist.empty:
                return {'error': f"Could not retrieve information for {symbol}. Symbol may not exist."}
            else:
                last_p = float(hist['Close'].iloc[-1]) if not hist.empty else 'N/A'
                vol = int(hist['Volume'].iloc[-1]) if not hist.empty else 'N/A'
                return {
                    'name': symbol,
                    'last_price': last_p,
                    'volume': vol,
                    'note': 'Limited information available'
                }
        
        return {
            'name': info.get('shortName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'dividend_yield': info.get('dividendYield', 'N/A'),
            'fifty_two_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
            'fifty_two_week_low': info.get('fiftyTwoWeekLow', 'N/A')
        }
        
    except Exception as e:
        return {'error': f"Could not retrieve information for {symbol}: {str(e)}"}

def get_stock_data(symbol, start_date, end_date, retries=3, delay=2):
    for attempt in range(retries):
        try:
            print(f"Attempt {attempt+1}: Downloading {symbol} from {start_date} to {end_date}")
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            if df.empty:
                print("Empty DataFrame returned by yfinance.")
                raise ValueError("Received empty data from yfinance.")

            # Flatten MultiIndex columns if present (yfinance >= 0.2.40)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            return df, None
        except Exception as e:
            print(f"Error downloading data: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                return None, f"Failed to fetch stock data for {symbol}: {str(e)}"

if __name__ == "__main__":
    symbol = "AAPL"
    print(f"Testing get_stock_info for {symbol}")
    print(get_stock_info(symbol))
    
    print(f"\nTesting get_stock_data for {symbol}")
    data, error = get_stock_data(symbol, "2023-01-01", "2023-12-31")
    if error:
        print(f"Error: {error}")
    else:
        print(f"Data shape: {data.shape}")
        print(data.head())
