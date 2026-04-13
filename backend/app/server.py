"""FastAPI application with CRUD endpoints for products and sales."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .db import engine, get_db, Base
from .entities import Product, Sale
from .dto import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    PaginatedProducts,
    SaleCreate,
    SaleResponse,
)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Inventory Forecast Dashboard API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/")
def health_check():
    """Simple liveness probe."""
    return {"status": "ok", "service": "inventory-forecast-dashboard"}


# ── Products ────────────────────────────────────────────────────────────────

@app.post("/products/", response_model=ProductResponse, status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    """Add a new product to the catalog."""
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products/", response_model=PaginatedProducts)
def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """Return a paginated list of products."""
    total = db.query(Product).count()
    offset = (page - 1) * page_size
    items = (
        db.query(Product)
        .order_by(Product.id)
        .offset(offset)
        .limit(page_size)
        .all()
    )
    return PaginatedProducts(items=items, total=total, page=page, page_size=page_size)


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product by ID."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)
):
    """Partially update a product."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Remove a product and its associated sales."""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()


# ── Sales ────────────────────────────────────────────────────────────────────

@app.post("/sales/", response_model=SaleResponse, status_code=201)
def record_sale(payload: SaleCreate, db: Session = Depends(get_db)):
    """Record a sale and decrement product stock."""
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.current_stock < payload.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    product.current_stock -= payload.quantity
    sale = Sale(**payload.model_dump())
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale


@app.get("/sales/", response_model=list[SaleResponse])
def list_sales(
    product_id: int | None = None,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
):
    """Return recent sales, optionally filtered by product."""
    query = db.query(Sale).order_by(Sale.sale_date.desc())
    if product_id is not None:
        query = query.filter(Sale.product_id == product_id)
    return query.limit(limit).all()
