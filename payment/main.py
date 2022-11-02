import time, requests
from typing import List
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from payment import schemas,models

from payment.database.database import get_db

app = FastAPI()

redis = get_redis_connection(
    host='redis',
    port=6379,
    password='',
    decode_responses=True
)

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
    "/orders/{order_id}/",
    response_model=schemas.OrderSchema,
    tags=["payment"],
)
def get_products(order_id:int, db: Session = Depends(get_db)):
    order = db.query(models.Order).get(order_id)
    return order

@app.get(
    "/orders",
    response_model=List[schemas.OrderSchema],
    tags=["payment"],
)
def get_products(db: Session = Depends(get_db)):
    orders = db.query(models.Order).all()
    return orders

@app.post(
    "/orders",
    tags=["payment"],
)
async def post_orders(
    request: schemas.OrderBaseSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    req = requests.get(f'http://inventory:8001/products/{request.product_id}')
    
    product = req.json()
    new_order = models.Order(
        product_id=product['id'], 
        price=product['price'], 
        quantity=request.quantity,
        fee=0.2*product['price'],
        total=1.2*product['price'],
        status='pending',
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    background_tasks.add_task(complete_order,new_order, db)
    
    return {"details": 'Order Added'}

def complete_order(order,db:Session):
    time.sleep(5)
    update_order = db.query(models.Order).filter(models.Order.id == order.id)
    update_order.update({'status':'completed'}, synchronize_session=False)
    db.commit()
    redis.xadd('order_completed',{'order':order.id},'*')
    

@app.delete(
    "/orders/{id}",
    tags=["payment"],
)
def delete_products(
    product_id,
    db: Session = Depends(get_db)
):
   pass