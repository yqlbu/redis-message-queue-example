import redis
from pydantic import BaseModel

stream = "demo"


# Define data model
class Event(BaseModel):
    eventType: str
    amount: int
    item_id: str


# Connect to a local redis instance
r = redis.Redis(host="localhost", port=6379, db=0)

# Construct data and create an event object
event_data = {"eventType": "purchase", "amount": 2, "item_id": "XXX"}
event: Event = Event(**event_data)

# Publish message to the stream
# the `*` means that redis generates and event id automatically
r.xadd(name=stream, id="*", fields={"message": event.model_dump_json()})  # type: ignore
