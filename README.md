# Stock Data Intelligence Dashboard

A simple stock market dashboard project built with FastAPI, SQLite, Pandas, and Chart.js. It collects Indian stock data, stores it locally, provides REST APIs, and shows the data in a browser dashboard.

## Live Demo

- App: `https://stock-dashboard-rinr.onrender.com`
- Dashboard: `https://stock-dashboard-rinr.onrender.com/static/dashboard.html`
- API Docs: `https://stock-dashboard-rinr.onrender.com/docs`

## Features

- Stock data collection using `yfinance`
- Data cleaning and storage in SQLite
- FastAPI backend with REST APIs
- Dashboard for stock charts and summary stats
- Top gainers and top losers
- 7-day moving average, 52-week high/low, and volatility
- Stock comparison between two companies

## Completed Assignment Tasks

- Historical stock data fetched and cleaned
- Data stored in a relational database
- API to list companies
- API to get last 30 days data for a stock
- API to get stock summary
- API to compare two stocks
- Frontend dashboard added

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- yfinance
- Chart.js

## Project Files

```text
app.py
database.py
data_collector.py
requirements.txt
stocks.db
static/dashboard.html
```

## Run Locally

```bash
git clone <your-repo-url>
cd stock-dashboard
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Open:

- `http://127.0.0.1:8000/`
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/static/dashboard.html`

## Refresh Stock Data

```bash
python data_collector.py
python app.py
```

## Main API Endpoints

- `GET /companies`
- `GET /data/{symbol}`
- `GET /summary/{symbol}`
- `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS&days=30`
- `GET /stocks/top-gainers`
- `GET /stocks/top-losers`

## Notes

- `stocks.db` is already included, so the project can run quickly after cloning
- Internet is needed only when downloading fresh stock data

## Author

Built by Rishabh for the JarNox assignment.
