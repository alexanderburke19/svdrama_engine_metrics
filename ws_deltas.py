import asyncio
import websockets
import json
from datetime import datetime, timezone

# Your Signal K server WebSocket endpoint
uri = "ws://10.10.10.1:3000/signalk/v1/stream?subscribe=none"

# Your bearer auth token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRyYW1hIiwiaWF0IjoxNzExNTA0NDc5LCJleHAiOjE3NDMwNDA0Nzl9.yQJSF0-AfTYSW5rW2JH1aWLzlX3j2KMaAYYDX-8yl6c"


def get_timestamp():
    """Create a timestamp in ISO 8601 format with milliseconds."""
    now_utc_with_tz = datetime.now(timezone.utc)
    timestamp_iso_with_ms = now_utc_with_tz.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return timestamp_iso_with_ms


async def send_delta(sk_path, new_value, metadata=None):
    """Send a SignalK delta message to the server with the specified path and value."""
    headers = {"Authorization": f"Bearer {token}"}

    try:
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
                delta_message["updates"][0]["meta"] = {sk_path: metadata}

            # Convert the delta message to JSON
            delta_json = json.dumps(delta_message)

            print(f"Sending delta message: {delta_json}")

            # Set a timeout for sending and receiving the message
            await asyncio.wait_for(websocket.send(delta_json), timeout=10)

            # Optionally, receive and log the server's response
            response = await asyncio.wait_for(websocket.recv(), timeout=10)
            print(f"Received response: {response}")

    except asyncio.TimeoutError:
        print("WebSocket connection timed out.")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"WebSocket connection closed with error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        print("WebSocket connection closed.")


def send_signal_k_delta(sk_path, new_value, metadata=None):
    """Send the SignalK delta asynchronously."""
    # Ensure event loop is running properly
    try:
        asyncio.get_event_loop().run_until_complete(
            send_delta(sk_path, new_value, metadata)
        )
    except RuntimeError as e:
        print(f"Event loop error: {e}")


# Example usage:
if __name__ == "__main__":
    # Example call to update RPM path with a value of 1500
    send_signal_k_delta("propulsion.main.revolutions", 1500)
