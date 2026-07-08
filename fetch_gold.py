import requests
from datetime import datetime

from database.database import get_session
from database.models import GoldPrice
from config import API_KEY


url = "https://www.alphavantage.co/query"

params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "GLD",
    "apikey": API_KEY
}


def fetch_gold():

    response = requests.get(url, params=params)

    data = response.json()

    if "Time Series (Daily)" not in data:
        print(data)
        return


    prices = data["Time Series (Daily)"]

    session = get_session()

    added = 0


    for date, values in prices.items():

        price_date = datetime.strptime(
            date,
            "%Y-%m-%d"
        ).date()


        existing = session.query(GoldPrice).filter_by(
            price_date=price_date
        ).first()


        if existing:
            continue


        gold = GoldPrice(

            price_date=price_date,

            price=float(values["4. close"]),

            source="AlphaVantage GLD"

        )


        session.add(gold)

        added += 1


    session.commit()

    session.close()


    print(f"Added {added} records")


if __name__ == "__main__":
    fetch_gold()