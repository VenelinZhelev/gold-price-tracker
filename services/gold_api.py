import requests
from datetime import datetime


SOURCE = "Frankfurter API"


def get_gold_prices(start_date, end_date):

    url = (
        f"https://api.frankfurter.app/"
        f"{start_date}..{end_date}"
        "?from=XAU&to=USD"
    )

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception("Cannot fetch data.")

    data = response.json()

    prices = []

    for day, value in data["rates"].items():

        record = {
            "date": datetime.strptime(
                day,
                "%Y-%m-%d"
            ).date(),

            "price": value["USD"],

            "source": SOURCE
        }

        prices.append(record)

    return prices