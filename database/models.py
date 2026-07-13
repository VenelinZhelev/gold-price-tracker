from database.database import Base
from sqlalchemy import Column, Integer, Numeric, Date, String, DateTime, Float, UniqueConstraint
from sqlalchemy.sql import func

from database.database import Base


class GoldPrice(Base):
    __tablename__ = "gold_prices"

    id = Column(Integer, primary_key=True)

    price_date = Column(
        Date,
        nullable=False,
        unique=True
    )

    price = Column(
        Float,
        nullable=False
    )

    currency = Column(
        String,
        default="USD",
        nullable=False
    )

    unit = Column(
        String,
        default="troy ounce",
        nullable=False
    )
    
    source = Column(
        String(100),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    __table_args__ = (
        UniqueConstraint(
            "price_date",
            "source",
            name="unique_price_source"
        ),
    )