from inventory.main import redis 
import time
key = 'order_completed'
group = 'inventory'

try:
    redis.xgroup_create(key, group)
except:
    print('Grpup already exist!')
    
while True:
    try:
        results = redis.xreadgroup(group, key, {key:'>'},None)
        print(results)
    except Exception as e:
        print(str((e)))
    time.sleep(1)