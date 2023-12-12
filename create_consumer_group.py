import redis

stream_key = "demo"
consumer_group = "consumer_group"

# Connect to a local redis instance
r = redis.Redis(host="localhost", port=6379, db=0)

# Create a consumer group
r.xgroup_create(stream_key, consumer_group, id="0", mkstream=True)
