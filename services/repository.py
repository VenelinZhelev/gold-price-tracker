from database.database import get_session
from database.models import GoldPrice


def save_price(record):
    session = get_session()

    existing = (
        session.query(GoldPrice)
        .filter_by(price_date=record["date"])
        .first()
    )

    if existing:
        session.close()
        return False

    price = GoldPrice(
        price_date=record["date"],
        price=record["price"],
        source=record["source"]
    )

    session.add(price)
    session.commit()
    session.close()

    return True


def get_latest_price():
    session = get_session()

    result = (
        session.query(GoldPrice)
        .order_by(GoldPrice.price_date.desc())
        .first()
    )

    session.close()

    return result


def get_price_by_date(target_date):
    session = get_session()

    result = (
        session.query(GoldPrice)
        .filter_by(price_date=target_date)
        .first()
    )

    session.close()

    return result


def get_prices_between(start, end):
    session = get_session()

    result = (
        session.query(GoldPrice)
        .filter(GoldPrice.price_date >= start)
        .filter(GoldPrice.price_date <= end)
        .all()
    )

    session.close()

    return result