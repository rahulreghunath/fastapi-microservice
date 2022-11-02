from typing import List
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from inventory import schemas,models

from inventory.database.database import get_db

app = FastAPI()

# cross origin resource sharing
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


redis = get_redis_connection(
    host='redis',
    port=6379,
    password='',
    decode_responses=True
)

@app.get(
    "/products",
    response_model=List[schemas.ProductSchema],
    tags=["inventory"],
)
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products
@app.get(
    "/products/{product_id}",
    response_model=schemas.ProductSchema,
    tags=["inventory"],
)
def get_product(product_id:int,db: Session = Depends(get_db)):
    
    product = db.query(models.Product).get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@app.post(
    "/products",
    tags=["inventory"],
)
def post_products(
    request: schemas.ProductBaseSchema,
    db: Session = Depends(get_db)
):
    new_product = models.Product(name=request.name, price=request.price, quantity=request.quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"details": 'Product Added'}

@app.delete(
    "/products/{product_id}",
    tags=["inventory"],
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