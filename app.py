from flask import Flask, jsonify, request, render_template
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
        "currency": row.currency,
        "unit": row.unit,
        "source": row.source
    }


@app.get("/chart")
def chart():
    return render_template("index.html")


@app.get("/latest")
def latest():

    row = get_latest_price()

    if not row:
        return jsonify({
            "error": "No data found"
        }), 404

    return jsonify(format_row(row))


@app.get("/price/<date_str>")
def by_date(date_str):

    try:
        target_date = datetime.strptime(
            date_str,
            "%Y-%m-%d"
        ).date()

    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400


    row = get_price_by_date(target_date)


    if not row:
        return jsonify({
            "error": "No price found for this date"
        }), 404


    return jsonify(format_row(row))



@app.get("/")
def home():

    return jsonify({
        "status": "ok",
        "endpoints": [
            "/chart",
            "/latest",
            "/price/<date>",
            "/prices?start=&end="
        ]
    })



@app.get("/prices")
def range_prices():

    start = request.args.get("start")
    end = request.args.get("end")


    if not start or not end:
        return jsonify({
            "error": "start and end are required"
        }), 400


    try:
        start_date = datetime.strptime(
            start,
            "%Y-%m-%d"
        ).date()

        end_date = datetime.strptime(
            end,
            "%Y-%m-%d"
        ).date()


    except ValueError:
        return jsonify({
            "error": "Invalid date format. Use YYYY-MM-DD"
        }), 400

    if start_date > end_date:
        return jsonify({
            "error": "start date cannot be after end date"
        }), 400



    rows = get_prices_between(
        start_date,
        end_date
    )


    if not rows:
        return jsonify({
            "error": "No data found for this period"
        }), 404



    return jsonify([
        format_row(row)
        for row in rows
    ])



if __name__ == "__main__":
    app.run(debug=True)