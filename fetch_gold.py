import requests
from datetime import datetime

from config import TWELVE_DATA_KEY
from database.database import get_session
from database.models import GoldPrice


URL = "https://api.twelvedata.com/time_series"


def fetch_gold():
    if not TWELVE_DATA_KEY:
        print("Missing API key")
        return

    params = {
        "symbol": "XAU/USD",
        "interval": "1day",
        "outputsize": 200,
        "apikey": TWELVE_DATA_KEY
    }


    try:
        response = requests.get(
            URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("status") == "error":
            print(data.get("message"))
            return

    except requests.RequestException as e:
        print(f"API error: {e}")
        return



    if "values" not in data or not data["values"]:
        print("No data returned from API")
        return



    session = get_session()

    try:

        added = 0

        for item in data["values"]:

            price_date = datetime.strptime(
                item["datetime"],
                "%Y-%m-%d"
            ).date()

            existing = session.query(GoldPrice).filter_by(
                price_date=price_date,
                source="Twelve Data XAU/USD"
            ).first()

            if existing:
                continue

            price = float(item["close"])

            if price <= 0:
                print(f"Invalid price for {price_date}")
                continue

            gold = GoldPrice(
                price_date=price_date,
                price=price,
                currency="USD",
                unit="troy ounce",
                source="Twelve Data XAU/USD"
            )

            session.add(gold)

            added += 1

        session.commit()

    finally:
        session.close()


    print(f"Added {added} gold records")



if __name__ == "__main__":
    fetch_gold()