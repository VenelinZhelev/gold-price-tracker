from datetime import date, timedelta

from services.gold_api import get_gold_prices
from services.repository import save_price
from services.validator import validate_record


def run_import(days_back=365 * 3):
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)

    print(f"Fetching data from {start_date} to {end_date}")

    data = get_gold_prices(start_date, end_date)

    inserted = 0
    skipped = 0

    for record in data:

        if not validate_record(record):
            skipped += 1
            continue

        if save_price(record):
            inserted += 1
        else:
            skipped += 1

    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")


if __name__ == "__main__":
    run_import()