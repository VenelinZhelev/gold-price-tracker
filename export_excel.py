import pandas as pd
import os

from database.database import get_session
from database.models import GoldPrice


session = get_session()


rows = (
    session.query(GoldPrice)
    .order_by(
        GoldPrice.price_date.desc()
    )
    .all()
)


print(f"Rows found: {len(rows)}")


data = []

for row in rows:
    data.append({
        "date": row.price_date,
        "price": row.price,
        "currency": row.currency,
        "unit": row.unit,
        "source": row.source,
        "created_at": (
            row.created_at.replace(tzinfo=None)
            if row.created_at
            else None
        )
    })


df = pd.DataFrame(data)


file_path = os.path.join(
    os.getcwd(),
    "gold_prices.xlsx"
)


df.to_excel(
    file_path,
    index=False
)


session.close()


print(f"Excel exported successfully: {file_path}")