from database.database import SessionLocal
from database.models import GoldPrice


def get_session():
    return SessionLocal()


def get_latest_price():
    session = get_session()
    return session.query(GoldPrice).order_by(GoldPrice.price_date.desc()).first()


def get_price_by_date(target_date):
    session = get_session()
    return session.query(GoldPrice).filter(GoldPrice.price_date == target_date).first()


def get_prices_between(start_date, end_date):
    session = get_session()
    return session.query(GoldPrice).filter(
        GoldPrice.price_date >= start_date,
        GoldPrice.price_date <= end_date
    ).all()