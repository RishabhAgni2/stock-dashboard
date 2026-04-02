"""Download stock data, clean it, compute metrics, and store it in SQLite."""

import pandas as pd
import yfinance as yf

from database import SessionLocal, StockData


STOCK_LIST = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "HINDUNILVR.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "BHARTIARTL.NS",
    "ITC.NS",
    "KOTAKBANK.NS",
]


def download_stock_data(symbol: str, period: str = "1y") -> pd.DataFrame | None:
    print(f"Downloading data for {symbol}...")

    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period, interval="1d")

        if data.empty:
            print(f"Warning: no data found for {symbol}")
            return None

        data = data.reset_index()
        data["Symbol"] = symbol
        print(f"Downloaded {len(data)} rows for {symbol}")
        return data
    except Exception as exc:
        print(f"Error downloading {symbol}: {exc}")
        return None


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")

    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
    for column in numeric_columns:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.dropna(subset=["Date", "Open", "High", "Low", "Close", "Volume"])
    cleaned = cleaned.sort_values("Date").drop_duplicates(subset=["Date"], keep="last")
    cleaned["Volume"] = cleaned["Volume"].fillna(0)

    return cleaned


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    enriched["Daily_Return"] = ((enriched["Close"] - enriched["Open"]) / enriched["Open"]) * 100
    enriched["MA_7"] = enriched["Close"].rolling(window=7).mean()
    enriched["Week_52_High"] = enriched["Close"].rolling(window=252, min_periods=1).max()
    enriched["Week_52_Low"] = enriched["Close"].rolling(window=252, min_periods=1).min()
    enriched["Volatility"] = enriched["Close"].rolling(window=30).std()
    enriched["Volume_MA_7"] = enriched["Volume"].rolling(window=7).mean()
    return enriched


def save_to_database(df: pd.DataFrame, symbol: str) -> None:
    db = SessionLocal()

    try:
        print(f"Cleaning old data for {symbol}...")
        db.query(StockData).filter(StockData.symbol == symbol).delete()

        print(f"Saving {len(df)} rows to database...")
        for _, row in df.iterrows():
            stock_entry = StockData(
                symbol=symbol,
                date=row["Date"].date(),
                open=float(row["Open"]),
                high=float(row["High"]),
                low=float(row["Low"]),
                close=float(row["Close"]),
                volume=int(row["Volume"]),
                daily_return=float(row["Daily_Return"]) if pd.notna(row["Daily_Return"]) else None,
                ma_7=float(row["MA_7"]) if pd.notna(row["MA_7"]) else None,
                week_52_high=float(row["Week_52_High"]) if pd.notna(row["Week_52_High"]) else None,
                week_52_low=float(row["Week_52_Low"]) if pd.notna(row["Week_52_Low"]) else None,
                volatility=float(row["Volatility"]) if pd.notna(row["Volatility"]) else None,
            )
            db.add(stock_entry)

        db.commit()
        print(f"Successfully saved {symbol} to database!")
    except Exception as exc:
        db.rollback()
        print(f"Error saving to database: {exc}")
    finally:
        db.close()


def main():
    print("\n" + "=" * 60)
    print("STOCK DATA COLLECTOR STARTED")
    print("=" * 60 + "\n")

    success_count = 0
    failed_count = 0

    for symbol in STOCK_LIST:
        print(f"\nProcessing {symbol}...")
        data = download_stock_data(symbol, period="1y")

        if data is None:
            failed_count += 1
            continue

        data = clean_stock_data(data)
        data = calculate_metrics(data)
        save_to_database(data, symbol)
        success_count += 1

    print("\n" + "=" * 60)
    print("DATA COLLECTION COMPLETE")
    print("=" * 60)
    print(f"Successfully processed: {success_count} stocks")
    print(f"Failed: {failed_count} stocks")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
