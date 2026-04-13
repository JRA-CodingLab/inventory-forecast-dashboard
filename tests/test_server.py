"""Tests for FastAPI server endpoints using a test client with mocked DB."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.app.db import Base, get_db
from backend.app.server import app


@pytest.fixture()
def client():
    """Create a test client with an in-memory SQLite database."""
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    TestSession = sessionmaker(bind=test_engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as tc:
        yield tc
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


class TestHealthCheck:
    def test_root_returns_ok(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "inventory" in data["service"].lower()


class TestProductEndpoints:
    def test_create_product(self, client):
        payload = {"name": "Alpha Widget", "category": "Widgets", "price": 29.99, "current_stock": 100}
        response = client.post("/products/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Alpha Widget"
        assert data["id"] is not None

    def test_create_product_invalid(self, client):
        payload = {"name": "", "category": "Widgets", "price": 29.99}
        response = client.post("/products/", json=payload)
        assert response.status_code == 422

    def test_list_products_empty(self, client):
        response = client.get("/products/")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_products_pagination(self, client):
        for i in range(5):
            client.post("/products/", json={
                "name": f"Product {i}",
                "category": "Batch",
                "price": 10.0,
                "current_stock": i * 10,
            })
        response = client.get("/products/?page=1&page_size=2")
        data = response.json()
        assert len(data["items"]) == 2
        assert data["total"] == 5
        assert data["page"] == 1

    def test_get_product_by_id(self, client):
        create_resp = client.post("/products/", json={
            "name": "Lookup Item", "category": "Test", "price": 5.0, "current_stock": 20,
        })
        pid = create_resp.json()["id"]
        response = client.get(f"/products/{pid}")
        assert response.status_code == 200
        assert response.json()["name"] == "Lookup Item"

    def test_get_product_not_found(self, client):
        response = client.get("/products/9999")
        assert response.status_code == 404

    def test_update_product(self, client):
        create_resp = client.post("/products/", json={
            "name": "Old Name", "category": "Cat", "price": 1.0, "current_stock": 10,
        })
        pid = create_resp.json()["id"]
        response = client.patch(f"/products/{pid}", json={"name": "New Name", "price": 2.50})
        assert response.status_code == 200
        assert response.json()["name"] == "New Name"
        assert response.json()["price"] == 2.50
        assert response.json()["category"] == "Cat"

    def test_update_product_not_found(self, client):
        response = client.patch("/products/9999", json={"name": "Ghost"})
        assert response.status_code == 404

    def test_delete_product(self, client):
        create_resp = client.post("/products/", json={
            "name": "Doomed", "category": "Temp", "price": 1.0, "current_stock": 0,
        })
        pid = create_resp.json()["id"]
        response = client.delete(f"/products/{pid}")
        assert response.status_code == 204
        assert client.get(f"/products/{pid}").status_code == 404

    def test_delete_product_not_found(self, client):
        response = client.delete("/products/9999")
        assert response.status_code == 404


class TestSaleEndpoints:
    def _create_product(self, client, stock=50):
        resp = client.post("/products/", json={
            "name": "Sale Target", "category": "Sales", "price": 10.0, "current_stock": stock,
        })
        return resp.json()["id"]

    def test_record_sale(self, client):
        pid = self._create_product(client, stock=50)
        response = client.post("/sales/", json={"product_id": pid, "quantity": 3})
        assert response.status_code == 201
        data = response.json()
        assert data["quantity"] == 3
        assert data["product_id"] == pid
        product = client.get(f"/products/{pid}").json()
        assert product["current_stock"] == 47

    def test_record_sale_insufficient_stock(self, client):
        pid = self._create_product(client, stock=2)
        response = client.post("/sales/", json={"product_id": pid, "quantity": 10})
        assert response.status_code == 400

    def test_record_sale_product_not_found(self, client):
        response = client.post("/sales/", json={"product_id": 9999, "quantity": 1})
        assert response.status_code == 404

    def test_list_sales(self, client):
        pid = self._create_product(client, stock=100)
        client.post("/sales/", json={"product_id": pid, "quantity": 5})
        client.post("/sales/", json={"product_id": pid, "quantity": 3})
        response = client.get("/sales/")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_sales_filter_by_product(self, client):
        pid1 = self._create_product(client, stock=100)
        pid2 = self._create_product(client, stock=100)
        client.post("/sales/", json={"product_id": pid1, "quantity": 2})
        client.post("/sales/", json={"product_id": pid2, "quantity": 4})
        response = client.get(f"/sales/?product_id={pid1}")
        sales = response.json()
        assert len(sales) == 1
        assert sales[0]["product_id"] == pid1
