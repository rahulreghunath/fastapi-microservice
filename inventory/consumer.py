from inventory.redis_app import redis 
import time
from inventory.database.database import get_db
from inventory import models
import asyncio
from contextlib import contextmanager

from fastapi.concurrency import contextmanager_in_threadpool

key = 'order_completed'
group = 'inventory'

db = get_db()

async def update_product(data):
    try:
        
        async with contextmanager_in_threadpool(contextmanager(get_db)()) as db:
            product = db.query(models.Product).get(data['product_id'])  
            
            product.quantity = product.quantity - int(data['quantity'])
            db.commit()
    except Exception as e:
        print(str((e)))
        
async def consume_data():
    try:
        redis.xgroup_create(key, group)
    except:
        print('Grpup already exist!')
        
    while True:
        try:
            results = redis.xreadgroup(group, key, {key:'>'},None)
            if results !=[]:
                for result in results:
                    data = result[1][0][1]           
                    await update_product(data)                         
                    # asyncio.run(update_product(data))
                    
        except Exception as e:
            print(str((e)))
        time.sleep(1)
    
if __name__ =='__main__':
    asyncio.run(consume_data())