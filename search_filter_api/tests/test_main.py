from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_products():
    response = client.get("/products")

    assert response.status_code == 200
    assert len(response.json()) == 7

def test_search_product():
    response = client.get("/products?q=MO")

    assert response.status_code == 200
    assert len(response.json()) == 3

def test_filter_by_min_price():
    response = client.get("/products?min_price=10000")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_filter_by_max_price():
    response = client.get("/products?max_price=1000")

    assert response.status_code == 200
    assert len(response.json()) == 3

def test_pagination_limit():
    response = client.get("/products?limit=2")

    assert response.status_code == 200
    assert len(response.json()) == 2

def test_pagination_offset():
    response = client.get("/products?limit=2&offset=2")

    assert response.status_code == 200
    assert [p["id"] for p in response.json()] == [3, 4]

def test_pagination_after_filtering():
    response = client.get("/products?category=Electronics&limit=2&offset=1")

    assert response.status_code == 200
    assert len(response.json()) == 2

    expected_ids = [2, 3]

    assert [p["id"] for p in response.json()] == expected_ids

def test_sort_by_price_ascending():
    response = client.get("/products?sort_by=price&order=asc")

    assert response.status_code == 200
    assert [p["id"] for p in response.json()] == [6, 3, 7, 2, 4, 5, 1]

def test_sort_by_name_descending():
    response = client.get("/products?sort_by=name&order=desc")

    assert response.status_code == 200
    assert [p["id"] for p in response.json()] == [6, 2, 5, 3, 1, 4, 7]

def test_sort_by_name_ascending():
    response = client.get("/products?sort_by=name&order=asc")

    assert response.status_code == 200
    assert [p["id"] for p in response.json()] == [7, 4, 1, 3, 5, 2, 6]