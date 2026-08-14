import redis

redis_client = redis.Redis(host='localhost',port=6379, decode_responses=True)

redis_client.zadd('leaderboard', {'rahul':100, 'john':200, 'alice':150, 'bob':50, 'charlie':75})

print(redis_client.zrange('leaderboard',0,-1,desc=True,withscores=True))