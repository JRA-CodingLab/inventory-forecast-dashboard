"""Pydantic schemas (DTOs) for request validation and response serialization."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Product Schemas ────────────────────────────────────────────────────────────────

class ProductCreate(BaseModel):
    """Payload for creating a new product."""

    name: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=128)
    price: float = Field(..., gt=0)
    current_stock: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    """Payload for partially updating an existing product."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    category: Optional[str] = Field(default=None, min_length=1, max_length=128)
    price: Optional[float] = Field(default=None, gt=0)
    current_stock: Optional[int] = Field(default=None, ge=0)


class ProductResponse(BaseModel):
    """Serialized product returned by the API."""

    id: int
    name: str
    category: str
    price: float
    current_stock: int

    model_config = {"from_attributes": True}


# ── Sale Schemas ───────────────────────────────────────────────────────────────────

class SaleCreate(BaseModel):
    """Payload for recording a new sale."""

    product_id: int
    quantity: int = Field(..., gt=0)


class SaleResponse(BaseModel):
    """Serialized sale returned by the API."""

    id: int
    product_id: int
    quantity: int
    sale_date: datetime

    model_config = {"from_attributes": True}


# ── Pagination Wrapper ───────────────────────────────────────────────────────────────

class PaginatedProducts(BaseModel):
    """Paginated list of products with total count."""

    items: list[ProductResponse]
    total: int
    page: int
    page_size: int
