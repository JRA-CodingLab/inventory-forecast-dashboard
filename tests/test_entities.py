"""Tests for ORM entity models."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.db import Base
from backend.app.entities import Product, Sale


@pytest.fixture()
def db_session():
    """Create an in-memory SQLite database for each test."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


class TestProductModel:
    def test_create_product(self, db_session):
        product = Product(name="Widget A", category="Gadgets", price=19.99, current_stock=50)
        db_session.add(product)
        db_session.commit()

        fetched = db_session.query(Product).first()
        assert fetched is not None
        assert fetched.name == "Widget A"
        assert fetched.category == "Gadgets"
        assert fetched.price == 19.99
        assert fetched.current_stock == 50

    def test_product_repr(self, db_session):
        product = Product(name="Bolt", category="Hardware", price=0.50, current_stock=1000)
        db_session.add(product)
        db_session.commit()
        assert "Bolt" in repr(product)

    def test_product_default_stock(self, db_session):
        product = Product(name="New Item", category="Misc", price=5.00)
        db_session.add(product)
        db_session.commit()
        assert product.current_stock == 0


class TestSaleModel:
    def test_create_sale_with_relationship(self, db_session):
        product = Product(name="Sensor X", category="Electronics", price=12.50, current_stock=100)
        db_session.add(product)
        db_session.commit()

        sale = Sale(product_id=product.id, quantity=5)
        db_session.add(sale)
        db_session.commit()

        assert sale.product_id == product.id
        assert sale.quantity == 5
        assert sale.sale_date is not None
        assert sale.product.name == "Sensor X"

    def test_cascade_delete(self, db_session):
        product = Product(name="Temp", category="Test", price=1.00, current_stock=10)
        db_session.add(product)
        db_session.commit()

        sale = Sale(product_id=product.id, quantity=2)
        db_session.add(sale)
        db_session.commit()

        db_session.delete(product)
        db_session.commit()

        assert db_session.query(Sale).count() == 0

    def test_sale_repr(self, db_session):
        product = Product(name="Item", category="Cat", price=1.00, current_stock=5)
        db_session.add(product)
        db_session.commit()
        sale = Sale(product_id=product.id, quantity=3)
        db_session.add(sale)
        db_session.commit()
        assert "qty=3" in repr(sale)
