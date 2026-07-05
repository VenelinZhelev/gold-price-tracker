from datetime import date
from services.validator import validate_record


def test_valid_record():
    assert validate_record({
        "date": date.today(),
        "price": 2500,
        "source": "API"
    }) is True


def test_negative_price():
    assert validate_record({
        "date": date.today(),
        "price": -10,
        "source": "API"
    }) is False


def test_missing_price():
    assert validate_record({
        "date": date.today(),
        "source": "API"
    }) is False