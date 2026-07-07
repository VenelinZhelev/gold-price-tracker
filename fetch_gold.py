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

    for date, values in prices.items():

        gold = GoldPrice(
            price_date=datetime.strptime(
                date,
                "%Y-%m-%d"
            ).date(),

            price=float(values["4. close"]),

            source="AlphaVantage GLD"
        )

        session.add(gold)

    session.commit()
    session.close()

    print("Gold prices saved successfully!")


if __name__ == "__main__":
    fetch_gold()