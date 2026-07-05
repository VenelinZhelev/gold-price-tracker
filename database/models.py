from database.database import Base
from sqlalchemy import Column, Integer, Numeric, Date, String, DateTime, Float
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

    source = Column(
        String(100),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )