import os
import requests
from datetime import datetime
from dotenv import load_dotenv

from database.database import SessionLocal
from database.models import GoldPrice

load_dotenv()

API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.metalpriceapi.com/v1/timeframe"


def fetch_data(start_date, end_date):
    params = {
        "api_key": API_KEY,
        "base": "USD",
        "currencies": "XAU",
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()


def validate(price, date_str):
    if not date_str or not price:
        return False
    if float(price) <= 0:
        return False
    return True


def save_to_db(data):
    session = SessionLocal()

    rates = data.get("rates", {})

    for date_str, value in rates.items():

        # API връща XAU -> злато
        price = value.get("XAU")

        if not validate(price, date_str):
            continue

        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

        # check duplicate
        exists = session.query(GoldPrice).filter_by(price_date=date_obj).first()
        if exists:
            continue

        row = GoldPrice(
            price_date=date_obj,
            price=float(price),
            source="MetalPriceAPI"
        )

        session.add(row)

    session.commit()
    session.close()


def run():
    # последни 3 години
    start_date = "2023-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")

    data = fetch_data(start_date, end_date)
    save_to_db(data)

    print("Data successfully fetched and stored.")


if __name__ == "__main__":
    run()