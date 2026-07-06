import requests
from datetime import datetime

from database.database import get_session
from database.models import GoldPrice
from config import GOLD_API_KEY


URL = "https://www.goldapi.io/api/XAU/USD"


headers = {
    "x-access-token": GOLD_API_KEY,
    "Content-Type": "application/json"
}


def fetch_gold_price():
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    data = response.json()

    return {
        "date": datetime.utcnow().date(),
        "price": data["price"],
        "source": "GoldAPI"
    }


def save_price():
    session = get_session()

    gold = fetch_gold_price()

    exists = session.query(GoldPrice).filter_by(
        price_date=gold["date"]
    ).first()

    if exists:
        print("Today's price already exists.")
        session.close()
        return

    row = GoldPrice(
        price_date=gold["date"],
        price=gold["price"],
        source=gold["source"]
    )

    session.add(row)
    session.commit()
    session.close()

    print("Gold price saved successfully.")


if __name__ == "__main__":
    save_price()