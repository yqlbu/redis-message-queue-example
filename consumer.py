import redis
import json
from pydantic import BaseModel

stream = "demo"
consumer_group = "consumer_group"


# Define data model
class Event(BaseModel):
    eventType: str
    amount: int
    item_id: str


# Connect to a local redis instance
r = redis.Redis(host="localhost", port=6379, db=0)

# Create a consumer group
# r.xgroup_create(stream, consumer_group, id="0", mkstream=True)

# Read messages from the stream using the consumer group
while True:
    # messages = r.xreadgroup(
    #     consumer_group, "consumer", {stream: ">"}, count=1, block=0
    # )  # never blocks receiving new messages from the stream
    messages = r.xreadgroup(
        consumer_group, "consumer", {stream: ">"}, count=1, block=2000
    )  # set block time to 2000 (2s) to wait for new messages from the stream; exit the loop
    if messages:
        message_id, message_data = messages[0][1][0]  # type: ignore
        decoded_message = json.loads(
            message_data[b"message"].decode("utf-8")
        )  # Decode the message data
        print(f"Received message ID {message_id}: {decoded_message}")
        # Process the message here (you can perform any desired operations)
        # Acknowledge the message after processing
        r.xack(stream, consumer_group, message_id)
        # Remove the last entry from the stream
        r.xdel(stream, message_id)
        print("Last entry deleted from the stream.")
    else:
        print("No new messages.")
        break  # Exit the loop if there are no more messages

# Get all the message from the stream
msg = r.xrevrange(stream, count=20)
print(msg)

# # Get the current length of the stream
print(r.xlen(stream))
