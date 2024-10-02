import asyncio
import websockets
import json
from datetime import datetime, timezone

# Your Signal K server WebSocket endpoint
uri = "ws://10.10.10.1:3000/signalk/v1/stream?subscribe=none"

# Your bearer auth token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRyYW1hIiwiaWF0IjoxNzExNTA0NDc5LCJleHAiOjE3NDMwNDA0Nzl9.yQJSF0-AfTYSW5rW2JH1aWLzlX3j2KMaAYYDX-8yl6c"


def get_timestamp():
    """Create a timestamp in ISO 8601 format with milliseconds. This is used to timestamp the SignalK delta message.

    Returns:
        string: Timestamp in ISO 8601 format with milliseconds
    """
    # Get the current UTC date and time with timezone information
    now_utc_with_tz = datetime.now(timezone.utc)
    # Format the datetime object to ISO 8601 format with milliseconds
    timestamp_iso_with_ms = now_utc_with_tz.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return timestamp_iso_with_ms


async def send_delta(sk_path, new_value, metadata=None):
    """Send a Signal K delta message to the server with the specified path and value.

    Args:
        sk_path (string): The Signal K path to update.
        new_value (various): The new value to set at the path.
        metadata (string, optional): The metadata for sk_path to set unit type and description. Defaults to None.
    """
    # Include the token in the connection headers
    headers = {"Authorization": f"Bearer {token}"}

    # Establish the WebSocket connection with headers
    async with websockets.connect(uri, extra_headers=headers) as websocket:

        timestamp = get_timestamp()
        delta_message = {
            "context": "vessels.self",
            "updates": [
                {
                    "source": {"label": "drama-python", "type": "python"},
                    "timestamp": timestamp,
                    "values": [{"path": sk_path, "value": new_value}],
                }
            ],
        }
        # Add metadata if provided
        if metadata:
            delta_message["updates"][0]["meta"] = {
                sk_path: metadata
            }  # Attach metadata to the path

        # Convert the delta message to a JSON string
        delta_json = json.dumps(delta_message)

        # Just before sending the delta message
        print("Sending delta message:", delta_json)

        # Send the delta message
        await websocket.send(delta_json)

        # After awaiting a response
        print("Awaiting server response...")

        # Optionally, you can wait for a response
        response = await websocket.recv()
        print(f"Received response: {response}")


def send_signal_k_delta(sk_path, new_value, metadata=None):
    """Add a Signal K delta message to async event loop to send the delta to SignalK asynchronusly.

    Args:
        sk_path (string): The Signal K path to update.
        new_value (various): The new value to set at the path.
        metadata (string, optional): The metadata for sk_path to set unit type and description. Defaults to None.
    """
    # Include the token in the connection headers
    asyncio.get_event_loop().run_until_complete(
        send_delta(sk_path, new_value, metadata=None)
    )
