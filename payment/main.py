from typing import List
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import requests

from payment import schemas,models

from payment.database.database import get_db

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
    "/orders",
    response_model=List[schemas.OrderSchema],
    tags=["blogs"],
)
def get_products(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders

@app.post(
    "/orders",
    tags=["blogs"],
)
def post_orders(
    request: schemas.OrderBaseSchema,
    db: Session = Depends(get_db)
):
    req = requests.get(f'http://inventory:8001/products/{request.product_id}')
    
    product = req.json()
    new_order = models.Order(
        product_id=product.id, 
        price=product.price, 
        quantity=request.quantity,
        fee=0.2*product.price,
        total=1.2*product.price,
        status=request.status,
    )
    # db.add(new_order)
    # db.commit()
    # db.refresh(new_order)
    # return {"details": 'Order Added'}

@app.delete(
    "/orders/{id}",
    tags=["blogs"],
)
def delete_products(
    product_id,
    db: Session = Depends(get_db)
):
   pass