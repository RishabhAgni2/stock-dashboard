# Stock Data Intelligence Dashboard

A complete stock market analytics project built with FastAPI, SQLite, Pandas, and a simple HTML dashboard. The app collects Indian stock market data, stores it locally, exposes REST APIs, and visualizes the results in a browser.

This repository is set up so someone can clone it from GitHub, install dependencies, start the server, and explore both the API and dashboard with minimal effort.

## Project Highlights

- FastAPI backend with interactive Swagger docs
- SQLite database for local, zero-config storage
- Stock data collection using `yfinance`
- Data cleaning and metric generation with Pandas
- HTML dashboard with Chart.js visualizations
- Assignment endpoints for listing stocks, recent data, summaries, and comparison
- Extra analytics endpoints for top gainers, top losers, and latest stock price

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pandas
- yfinance
- Chart.js

## Features Implemented

### Core assignment tasks

- Store stock data in a relational database
- Fetch and clean historical stock market data
- Build APIs for:
- Company listing
- Last 30 days of stock data
- Stock summary statistics
- Two-stock comparison over a selected period

### Additional enhancements

- Interactive stock dashboard UI
- Top gainers endpoint
- Top losers endpoint
- Latest stock snapshot endpoint
- Configurable time range in the dashboard
- 7-day moving average
- 52-week high and low
- Volatility calculation

## Project Structure

```text
stock-dashboard/
|-- app.py                # FastAPI app and API routes
|-- database.py           # SQLAlchemy setup and schema
|-- data_collector.py     # Stock download, cleaning, metrics, DB save
|-- requirements.txt      # Python dependencies
|-- stocks.db             # SQLite database with stock data
|-- static/
|   |-- dashboard.html    # Frontend dashboard
```

## Supported Stocks

The current dataset includes these NSE symbols:

- `RELIANCE.NS`
- `TCS.NS`
- `HDFCBANK.NS`
- `INFY.NS`
- `HINDUNILVR.NS`
- `ICICIBANK.NS`
- `SBIN.NS`
- `BHARTIARTL.NS`
- `ITC.NS`
- `KOTAKBANK.NS`

## Quick Start

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd stock-dashboard
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

The server starts at:

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`
- Dashboard: `http://127.0.0.1:8000/static/dashboard.html`

## Fresh Data Setup

This repository already includes `stocks.db`, so the app can run immediately.

If you want to regenerate the database with fresh market data:

```bash
python data_collector.py
python app.py
```

## How the App Works

### Data pipeline

1. `data_collector.py` downloads 1 year of daily stock data using `yfinance`
2. The data is cleaned and normalized with Pandas
3. Metrics are calculated: daily return, 7-day moving average, 52-week high, 52-week low, and 30-day volatility
4. Processed rows are saved into SQLite (`stocks.db`)

### API layer

`app.py` reads from the database and exposes REST endpoints for analytics and dashboard consumption.

### Frontend

`static/dashboard.html` fetches data from the API and shows:

- Available stocks
- Summary cards
- Historical close-price chart
- 7-day moving average
- Top gainers and top losers

## API Endpoints

### Assignment endpoints

- `GET /companies`  
  List all companies stored in the database

- `GET /data/{symbol}`  
  Return the last 30 days of stock data for a symbol

- `GET /summary/{symbol}`  
  Return summary statistics for a symbol

- `GET /compare?symbol1=INFY.NS&symbol2=TCS.NS&days=30`  
  Compare two stocks by return, volume, and volatility

### Additional endpoints

- `GET /stocks/list`
- `GET /stocks/{symbol}`
- `GET /stocks/{symbol}/latest`
- `GET /stocks/top-gainers?limit=5`
- `GET /stocks/top-losers?limit=5`
- `GET /stocks/compare?symbol1=INFY.NS&symbol2=TCS.NS&days=30`

## Example API Usage

```bash
curl http://127.0.0.1:8000/companies
curl http://127.0.0.1:8000/data/INFY.NS
curl "http://127.0.0.1:8000/summary/TCS.NS"
curl "http://127.0.0.1:8000/compare?symbol1=INFY.NS&symbol2=TCS.NS&days=90"
```

## Why This Repo Is Easy To Run

- No external database setup required
- SQLite file is already included
- No API key required
- Simple dependency installation
- Dashboard and API run from the same FastAPI server
- Interactive docs available through Swagger UI

## Notes

- Internet is required only when running `data_collector.py` to download fresh stock data
- The dashboard depends on the backend running locally on `127.0.0.1:8000`
- The included database helps reviewers run the project instantly without waiting for a fresh download

## Submission Status

All major requested tasks for this project are implemented:

- Data collection
- Data cleaning
- Database storage
- REST API development
- Summary analytics
- Stock comparison
- Dashboard visualization

## Author

Built by Rishabh for the JarNox stock dashboard assignment.
