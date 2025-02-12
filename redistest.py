import redis

r = redis.Redis(
    host='fly-silflores-redis.upstash.io',
    port=6379,
    password='432c4aac83564bb08a597099aeeb1011',
    ssl=True,
    ssl_cert_reqs=None
)

print(r.ping())

# redis-cli -h fly-silflores-redis.upstash.io -p 6379 -a 432c4aac83564bb08a597099aeeb1011