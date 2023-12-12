import redis
import json

stream_key = "demo"
error_stream_key = "error_stream"
consumer_group = "consumer_group"

# Connect to a local redis instance
r = redis.Redis(host="localhost", port=6379, db=0)


def process_message(message_id, message_data):
    try:
        decoded_message = json.loads(
            message_data[b"message"].decode("utf-8")
        )  # Decode the message data

        # Process the message here (you can perform any desired operations)
        # TODO:
        # Add business logic here

        # Simulate processing (you can perform any desired operations)
        # For demonstration purposes, assume processing fails for odd-numbered messages
        # if decoded_message["id"] % 2 != 0:
        #     raise Exception("Failed to process message")
        print(f"Received message ID {message_id}: {decoded_message}")

        # Acknowledge the message after processing
        r.xack(stream_key, consumer_group, message_id)
    except Exception as err:
        print(f"Error processing message {message_id}: {err}")
        handle_error(message_id, message_data)


def handle_error(message_id, message_data):
    retries = int(message_data[b"retries"]) if b"retries" in message_data else 0
    if retries < 3:
        retries += 1
        # Update retries count and requeue the message back to the stream with updated metadata
        r.xadd(
            stream_key, {"content": message_data[b"content"], "retries": str(retries)}
        )
        # Acknowledge the original message to remove it from the pending list
        r.xack(stream_key, consumer_group, message_id)
        print(f"Message ID {message_id} requeued for retry ({retries}/3).")
    else:
        # Move the message to an error stream after reaching the maximum retry count
        r.xadd(
            error_stream_key,
            {"content": message_data[b"content"], "error": "Reached maximum retries"},
        )
        # Acknowledge the original message to remove it from the pending list
        r.xack(stream_key, consumer_group, message_id)
        print(f"Message ID {message_id} moved to error stream.")


# Process pending messages if any
pending_messages = r.xpending(stream_key, consumer_group)
if pending_messages:
    for message_info in pending_messages["pending"]:  # type: ignore
        message_id = message_info["message_id"]
        message_data = r.xrange(stream, min=message_id, max=message_id)[0][1]  # type: ignore
        process_message(message_id, message_data)

# Read messages from the stream using the consumer group
while True:
    messages = r.xreadgroup(
        consumer_group, "consumer", {stream_key: ">"}, count=1, block=10 * 1000
    )  # set block time to 10 * 1000 (10s) to wait for new messages from the stream; exit the loop; set block=0 for non-blocking state
    if messages:
        message_id, message_data = messages[0][1][0]  # type: ignore
        process_message(message_id, message_data)
    else:
        print("No new messages.")
        break  # Exit the loop if there are no more messages
