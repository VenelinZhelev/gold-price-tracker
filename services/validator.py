from datetime import date


def validate_record(record):
    """
    Проверява дали записът е валиден.
    """

    if "date" not in record:
        return False

    if "price" not in record:
        return False

    if "source" not in record:
        return False

    if record["date"] is None:
        return False

    if record["price"] is None:
        return False

    if record["source"] == "":
        return False

    if not isinstance(record["date"], date):
        return False

    try:
        price = float(record["price"])
    except ValueError:
        return False

    if price <= 0:
        return False

    return True