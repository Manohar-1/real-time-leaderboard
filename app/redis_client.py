import redis

redis_client = redis.Redis(host='localhost',port=6379, decode_responses=True)

#docker exec -it leaderboard-redis redis-cli ZREVRANGE global_leaderboard 0 -1 WITHSCORES