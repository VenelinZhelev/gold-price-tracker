def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_invalid_date(client):
    response = client.get("/price/test")
    assert response.status_code == 400


def test_missing_range(client):
    response = client.get("/prices")
    assert response.status_code == 400