# 📈 Stock Market Price Prediction System

An end-to-end Machine Learning & Web Application for predicting future stock market prices using **Long Short-Term Memory (LSTM)** deep learning neural networks, **Yahoo Finance API**, and **Flask**.

---

## 🌟 Key Features

- **Real-Time Data Integration**: Downloads historical stock data dynamically from Yahoo Finance (`yfinance`).
- **LSTM Deep Learning Architecture**: Trained on historical close prices (60-day sequence length) with Early Stopping & Dropout regularization.
- **Multi-Day Forecasting**: Predicts future stock prices for 1 to 30 business days ahead.
- **Model Evaluation Metrics**: Reports **RMSE**, **MAE**, **MAPE**, **R-squared ($R^2$)**, and **Directional Accuracy (%)**.
- **Interactive Visualizations**: Generates dynamic plots comparing historical values, test model predictions, and future price trends.
- **Modern Web UI**: Responsive Bootstrap 5 interface with real-time ticker info lookup.

---

## 📁 Repository Structure

```
portfolio/
├── app.py                 # Flask web server & route handlers
├── data_handler.py        # Yahoo Finance data fetcher & info parser
├── model.py               # TensorFlow/Keras LSTM model building & sequence prediction
├── utils.py               # Evaluation metrics (RMSE, MAE, MAPE, R2, Directional Accuracy)
├── requirements.txt       # Python package dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore configuration
├── .vscode/
│   └── launch.json        # VS Code launch & debug setup
├── static/
│   ├── css/
│   │   └── style.css      # Custom UI styles
│   └── js/
│       └── script.js      # Frontend interactivity & API fetch
└── templates/
    ├── index.html         # Homepage form interface
    ├── result.html        # Prediction results & plots display
    └── error.html         # User-friendly error page
```

---

## 🚀 Quick Start Guide in VS Code

### 1. Requirements & Prerequisites
Make sure Python 3.9+ is installed on your system.

### 2. Install Dependencies
Open a terminal in VS Code (`Ctrl + ~`) and run:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
You can run the application in any of the following ways:

#### Option A: Direct Python Command
```bash
python app.py
```

#### Option B: VS Code Run/Debug (F5)
Press **F5** in VS Code or click the **Play Button** in the top right corner while `app.py` is open.

---

## 🌐 Usage

1. Launching `app.py` automatically opens your default browser at `http://127.0.0.1:5000`.
2. Enter a stock symbol (e.g., `AAPL`, `MSFT`, `NVDA`, `TSLA`, `GOOGL`).
3. Click **Get Info** to view company sector, market cap, and 52-week range.
4. Select historical Start/End dates (recommended range $\ge$ 1 year) and the number of days to predict (e.g. 7 days).
5. Click **Predict Stock Prices**. The LSTM neural network will train on the data and render full metrics, price forecast tables, and trend plots.

---

## 📊 Performance Metrics

| Metric | Definition |
| :--- | :--- |
| **RMSE** | Root Mean Square Error — measures model standard deviation of error. |
| **MAE** | Mean Absolute Error — average dollar magnitude of prediction error. |
| **MAPE** | Mean Absolute Percentage Error — percentage discrepancy relative to actual prices. |
| **$R^2$ Score** | Coefficient of Determination — proportion of variance explained by model (up to 1.0). |
| **Directional Accuracy** | Percentage of days the model correctly predicted upward vs. downward price movements. |

---

## ⚠️ Disclaimer
*This tool is created for educational and research purposes only. Stock market price predictions are inherently uncertain and should not be used as financial advice.*
