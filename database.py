"""Database models and session setup for the stock dashboard."""

from sqlalchemy import Column, Date, Float, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./stocks.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class StockData(Base):
    __tablename__ = "stock_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    date = Column(Date, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    daily_return = Column(Float, nullable=True)
    ma_7 = Column(Float, nullable=True)
    week_52_high = Column(Float, nullable=True)
    week_52_low = Column(Float, nullable=True)
    volatility = Column(Float, nullable=True)

    def __repr__(self):
        return f"<StockData(symbol={self.symbol}, date={self.date}, close={self.close})>"


def init_database():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    print("Database file: stocks.db")
    print("Tables created: stock_data")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA:")
    print("=" * 60)
    print(
        """
    Table: stock_data
    Columns:
    - id (Integer, Primary Key)
    - symbol (String)
    - date (Date)
    - open (Float)
    - high (Float)
    - low (Float)
    - close (Float)
    - volume (Integer)
    - daily_return (Float, nullable)
    - ma_7 (Float, nullable)
    - week_52_high (Float, nullable)
    - week_52_low (Float, nullable)
    - volatility (Float, nullable)
    """
    )
    print("=" * 60)
