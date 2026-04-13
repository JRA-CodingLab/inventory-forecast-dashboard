"""ORM models for product inventory and sales tracking."""

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship

from .db import Base


class Product(Base):
    """Represents a product in the inventory catalog."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(128), nullable=False, index=True)
    price = Column(Float, nullable=False)
    current_stock = Column(Integer, nullable=False, default=0)

    sales = relationship("Sale", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} stock={self.current_stock}>"


class Sale(Base):
    """Records an individual sale transaction linked to a product."""

    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    sale_date = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    product = relationship("Product", back_populates="sales")

    __table_args__ = (
        Index("ix_sales_product_date", "product_id", "sale_date"),
    )

    def __repr__(self) -> str:
        return f"<Sale id={self.id} product_id={self.product_id} qty={self.quantity}>"
