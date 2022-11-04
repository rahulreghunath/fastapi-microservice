from typing import List
from typing import Union
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from inventory import schemas, models
from inventory.redis_app import redis

from inventory.database.database import get_db


router = APIRouter(
    prefix="/api/inventory",
    tags=["inventory"],
)


@router.get(
    "/products",
    response_model=List[schemas.ProductSchema],
)
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@router.get(
    "/products/{product_id}",
    response_model=schemas.ProductSchema,
    tags=["inventory"],
)
def get_product(product_id: int, db: Session = Depends(get_db)):

    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post(
    "/products",
)
def post_products(
    request: schemas.ProductBaseSchema,
    db: Session = Depends(get_db)
):
    new_product = models.Product(
        name=request.name, price=request.price, quantity=request.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"details": 'Product Added'}


@router.delete(
    "/products/{product_id}",    
)
def delete_products(
    product_id,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.id == product_id)

    if not product.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    product.delete(synchronize_session=False)

    db.commit()

    return {"details": "Product deleted"}
