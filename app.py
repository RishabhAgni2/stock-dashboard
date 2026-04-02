"""FastAPI backend for the stock dashboard."""

from datetime import datetime, timedelta
from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database import SessionLocal, StockData, init_database


app = FastAPI(
    title="Stock Data Intelligence Dashboard",
    description="REST API for Indian stock market data analysis",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def serialize_stock_row(row: StockData) -> dict:
    return {
        "date": str(row.date),
        "open": row.open,
        "high": row.high,
        "low": row.low,
        "close": row.close,
        "volume": row.volume,
        "daily_return": row.daily_return,
        "ma_7": row.ma_7,
        "week_52_high": row.week_52_high,
        "week_52_low": row.week_52_low,
        "volatility": row.volatility,
    }


@app.get("/", tags=["Home"])
def read_root():
    return {
        "message": "Welcome to Stock Data Intelligence Dashboard API",
        "documentation": "/docs",
        "dashboard": "/static/dashboard.html",
        "assignment_endpoints": {
            "companies": "/companies",
            "data": "/data/{symbol}",
            "summary": "/summary/{symbol}",
            "compare": "/compare?symbol1=INFY.NS&symbol2=TCS.NS",
        },
        "extra_endpoints": {
            "stocks_list": "/stocks/list",
            "latest_price": "/stocks/{symbol}/latest",
            "top_gainers": "/stocks/top-gainers",
            "top_losers": "/stocks/top-losers",
        },
    }


@app.get("/companies", tags=["Assignment"])
@app.get("/stocks/list", tags=["Stocks"])
def list_companies(db: Session = Depends(get_db)):
    companies = (
        db.query(
            StockData.symbol,
            func.count(StockData.id).label("data_points"),
        )
        .group_by(StockData.symbol)
        .order_by(StockData.symbol)
        .all()
    )

    return [
        {
            "symbol": company.symbol,
            "data_points": company.data_points,
        }
        for company in companies
    ]


@app.get("/stocks/top-gainers", tags=["Analytics"])
def top_gainers(
    limit: int = Query(5, description="Number of top stocks to return"),
    db: Session = Depends(get_db),
):
    from sqlalchemy import and_

    subquery = (
        db.query(
            StockData.symbol,
            func.max(StockData.date).label("max_date"),
        )
        .group_by(StockData.symbol)
        .subquery()
    )

    results = (
        db.query(StockData)
        .join(
            subquery,
            and_(
                StockData.symbol == subquery.c.symbol,
                StockData.date == subquery.c.max_date,
            ),
        )
        .filter(StockData.daily_return.isnot(None))
        .order_by(desc(StockData.daily_return))
        .limit(limit)
        .all()
    )

    return [
        {
            "symbol": row.symbol,
            "date": str(row.date),
            "close": row.close,
            "daily_return": round(row.daily_return, 2),
        }
        for row in results
    ]


@app.get("/stocks/top-losers", tags=["Analytics"])
def top_losers(
    limit: int = Query(5, description="Number of bottom stocks to return"),
    db: Session = Depends(get_db),
):
    from sqlalchemy import and_

    subquery = (
        db.query(
            StockData.symbol,
            func.max(StockData.date).label("max_date"),
        )
        .group_by(StockData.symbol)
        .subquery()
    )

    results = (
        db.query(StockData)
        .join(
            subquery,
            and_(
                StockData.symbol == subquery.c.symbol,
                StockData.date == subquery.c.max_date,
            ),
        )
        .filter(StockData.daily_return.isnot(None))
        .order_by(StockData.daily_return)
        .limit(limit)
        .all()
    )

    return [
        {
            "symbol": row.symbol,
            "date": str(row.date),
            "close": row.close,
            "daily_return": round(row.daily_return, 2),
        }
        for row in results
    ]


@app.get("/compare", tags=["Assignment"])
@app.get("/stocks/compare", tags=["Analytics"])
def compare_stocks(
    symbol1: str = Query(..., description="First stock symbol"),
    symbol2: str = Query(..., description="Second stock symbol"),
    days: int = Query(30, description="Number of days to compare"),
    db: Session = Depends(get_db),
):
    cutoff_date = datetime.now().date() - timedelta(days=days)

    data1 = (
        db.query(StockData)
        .filter(StockData.symbol == symbol1, StockData.date >= cutoff_date)
        .all()
    )
    data2 = (
        db.query(StockData)
        .filter(StockData.symbol == symbol2, StockData.date >= cutoff_date)
        .all()
    )

    if not data1 or not data2:
        raise HTTPException(status_code=404, detail="Insufficient data for comparison")

    valid_returns1 = [row.daily_return for row in data1 if row.daily_return is not None]
    valid_returns2 = [row.daily_return for row in data2 if row.daily_return is not None]
    valid_volatility1 = [row.volatility for row in data1 if row.volatility is not None]
    valid_volatility2 = [row.volatility for row in data2 if row.volatility is not None]

    avg_return1 = sum(valid_returns1) / len(valid_returns1) if valid_returns1 else 0
    avg_return2 = sum(valid_returns2) / len(valid_returns2) if valid_returns2 else 0
    avg_volume1 = sum(row.volume for row in data1) / len(data1)
    avg_volume2 = sum(row.volume for row in data2) / len(data2)
    avg_volatility1 = sum(valid_volatility1) / len(valid_volatility1) if valid_volatility1 else 0
    avg_volatility2 = sum(valid_volatility2) / len(valid_volatility2) if valid_volatility2 else 0

    return {
        "period_days": days,
        "symbol1": {
            "symbol": symbol1,
            "avg_daily_return": round(avg_return1, 2),
            "avg_volume": int(avg_volume1),
            "avg_volatility": round(avg_volatility1, 2),
        },
        "symbol2": {
            "symbol": symbol2,
            "avg_daily_return": round(avg_return2, 2),
            "avg_volume": int(avg_volume2),
            "avg_volatility": round(avg_volatility2, 2),
        },
        "winner": symbol1 if avg_return1 > avg_return2 else symbol2,
    }


@app.get("/data/{symbol}", tags=["Assignment"])
def get_last_30_days(symbol: str, db: Session = Depends(get_db)):
    return get_stock_data(symbol=symbol, days=30, start_date=None, end_date=None, db=db)


@app.get("/summary/{symbol}", tags=["Assignment"])
def get_summary(symbol: str, db: Session = Depends(get_db)):
    rows = (
        db.query(StockData)
        .filter(StockData.symbol == symbol)
        .order_by(StockData.date.desc())
        .limit(252)
        .all()
    )

    if not rows:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")

    closes = [row.close for row in rows]
    latest = rows[0]

    return {
        "symbol": symbol,
        "latest_date": str(latest.date),
        "days_considered": len(rows),
        "week_52_high": max(closes),
        "week_52_low": min(closes),
        "average_close": round(sum(closes) / len(closes), 2),
        "latest_close": latest.close,
        "latest_volatility": latest.volatility,
    }


@app.get("/stocks/{symbol}/latest", tags=["Stocks"])
def get_latest_price(symbol: str, db: Session = Depends(get_db)):
    latest = (
        db.query(StockData)
        .filter(StockData.symbol == symbol)
        .order_by(desc(StockData.date))
        .first()
    )

    if not latest:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")

    return {
        "symbol": symbol,
        "date": str(latest.date),
        "open": latest.open,
        "high": latest.high,
        "low": latest.low,
        "close": latest.close,
        "volume": latest.volume,
        "daily_return": latest.daily_return,
        "ma_7": latest.ma_7,
    }


@app.get("/stocks/{symbol}", tags=["Stocks"])
def get_stock_data(
    symbol: str,
    days: Optional[int] = Query(None, description="Number of recent days to fetch"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    query = db.query(StockData).filter(StockData.symbol == symbol)

    if days:
        cutoff_date = datetime.now().date() - timedelta(days=days)
        query = query.filter(StockData.date >= cutoff_date)

    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        query = query.filter(StockData.date >= start)

    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(StockData.date <= end)

    results = query.order_by(StockData.date).all()

    if not results:
        raise HTTPException(status_code=404, detail=f"No data found for symbol: {symbol}")

    return {
        "symbol": symbol,
        "count": len(results),
        "data": [serialize_stock_row(row) for row in results],
    }


@app.on_event("startup")
def startup_event():
    print("\n" + "=" * 60)
    print("Starting Stock Data Intelligence Dashboard")
    print("=" * 60)
    init_database()
    print("Server is ready!")
    print("API Documentation: http://127.0.0.1:8000/docs")
    print("Dashboard: http://127.0.0.1:8000/static/dashboard.html")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
