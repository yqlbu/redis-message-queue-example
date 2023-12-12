import redis

stream_key = "demo"
consumer_group = "consumer_group"

# Connect to a local redis instance
r = redis.Redis(host="localhost", port=6379, db=0)

# Get all the message from the stream
msg = r.xrevrange(stream_key, count=20)
print(msg)

# # Get the current length of the stream
print(r.xlen(stream_key))
