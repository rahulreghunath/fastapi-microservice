from redis_om import get_redis_connection

redis = get_redis_connection(
    host='redis',
    port=6379,
    password='',
    decode_responses=True
)