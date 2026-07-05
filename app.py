from flask import Flask, jsonify, request
from datetime import datetime

from services.repository import (
    get_latest_price,
    get_price_by_date,
    get_prices_between
)

app = Flask(__name__)


def format_row(row):
    if not row:
        return None

    return {
        "date": row.price_date.isoformat(),
        "price": float(row.price),
        "source": row.source
    }


@app.get("/latest")
def latest():
    row = get_latest_price()
    return jsonify(format_row(row))


@app.get("/price/<date_str>")
def by_date(date_str):
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    row = get_price_by_date(target_date)
    return jsonify(format_row(row))

@app.get("/")
def home():
    return jsonify({
        "status": "ok",
        "endpoints": ["/latest", "/price/<date>", "/prices?start=&end="]
    })
@app.get("/prices")
def range_prices():
    start = request.args.get("start")
    end = request.args.get("end")

    try:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
    except:
        return jsonify({"error": "Invalid date range"}), 400

    rows = get_prices_between(start_date, end_date)

    return jsonify([
        format_row(r) for r in rows
    ])


if __name__ == "__main__":
    app.run(debug=True)