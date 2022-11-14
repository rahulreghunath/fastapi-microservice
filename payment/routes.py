import time
import requests
from typing import List
from fastapi.background import BackgroundTasks
from typing import Union
from redis_om import get_redis_connection
from fastapi import FastAPI, Depends,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from payment import schemas, models, permission
from payment.oauth2 import get_current_user
from payment.database.database import get_db
from payment.redis_app import redis

router = APIRouter(
    prefix="/api/payment",
    tags=["payment"],
)

@router.get(
    "/orders/{order_id}/",
    response_model=schemas.OrderSchema,
    tags=["payment"],
)
def get_products(order_id: int, db: Session = Depends(get_db)):
    order = db.query(models.Order).get(order_id)
    return order


@router.get(
    "/orders",
    response_model=List[schemas.OrderSchema],
    tags=["payment"],
)
def get_products(
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(get_current_user),
):
    orders = db.query(models.Order).all()
    return orders


@router.post(
    "/orders",
    tags=["payment"],
)
async def post_orders(
    request: schemas.OrderBaseSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: schemas.TokenData = Depends(get_current_user),
):
    permission.check_permission(user,"can-add-order")
    
    req = requests.get(f'http://inventory:8001/api/inventory/products/{request.product_id}')

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
    background_tasks.add_task(complete_order, new_order, db)

    return {"details": 'Order Added'}


def complete_order(order, db: Session):
    time.sleep(5)
    update_order = db.query(models.Order).filter(
        models.Order.id == order.id
    )
    update_order.update({'status': 'completed'}, synchronize_session=False)
    db.commit()

    data  = {
        'id': order.id,
        'product_id':order.product_id,
        'quantity':order.quantity
    }


    redis.xadd('order_completed', data, '*')


@router.delete(
    "/orders/{id}",
    tags=["payment"],
)
def delete_products(
    product_id,
    db: Session = Depends(get_db)
):
    pass
