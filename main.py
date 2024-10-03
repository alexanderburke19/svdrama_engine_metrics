#!/usr/bin/env python3

import asyncio
import websockets
import json
from datetime import datetime, timezone
import yaml
import ws_deltas as ws
import utilities as utils
import fuel_consumption as fuel
import torque as torque
import power as power

# Fuel in tank in liters
fuel_in_tank = 100  # in liters

# Your SignalK server WebSocket endpoint
uri = "ws://10.10.10.1:3000/signalk/v1/stream"

# Your bearer auth token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRyYW1hIiwiaWF0IjoxNzExNTA0NDc5LCJleHAiOjE3NDMwNDA0Nzl9.yQJSF0-AfTYSW5rW2JH1aWLzlX3j2KMaAYYDX-8yl6c"


# Load the YAML configuration file
def load_paths():
    with open("yaml/paths.yaml", "r") as file:
        try:
            config = yaml.safe_load(file)
            return config
        except yaml.YAMLError as exc:
            print(exc)
            return None


config = load_paths()  # Load the YAML config


def get_timestamp():
    """Create a timestamp in ISO 8601 format with milliseconds."""
    now_utc_with_tz = datetime.now(timezone.utc)
    timestamp_iso_with_ms = now_utc_with_tz.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
    return timestamp_iso_with_ms


async def receive_data():
    """Subscribe to SignalK data and receive updates."""
    headers = {"Authorization": f"Bearer {token}"}
    while True:
        try:
            async with websockets.connect(uri, extra_headers=headers) as websocket:
                subscription_message = {
                    "context": "vessels.self",
                    "subscribe": [
                        {
                            "path": "propulsion.main.revolutions",
                            "minPeriod": 1000,  # Update period in milliseconds (1 second)
                        }
                    ],
                }

                # Send subscription message
                await websocket.send(json.dumps(subscription_message))
                print("Subscribed to 'propulsion.main.revolutions'")

                # Continuously receive data
                while True:
                    message = await websocket.recv()
                    data = json.loads(message)

                    if "updates" in data:
                        for update in data["updates"]:
                            for value in update["values"]:
                                if value["path"] == "propulsion.main.revolutions":
                                    rpm_value = value["value"]
                                    print(f"Received RPM value: {rpm_value}")

                                    # Transform data and send it back via the same WebSocket connection
                                    await transform_data(websocket, rpm_value)

        except (websockets.exceptions.ConnectionClosed, ConnectionError) as e:
            print(f"WebSocket connection lost: {e}. Reconnecting...")
            await asyncio.sleep(5)  # Wait before reconnecting

        finally:
            # Ensure that the WebSocket is closed properly
            if not websocket.closed:
                await websocket.close()
            print("WebSocket connection closed.")


async def transform_data(websocket, rpm):
    """Transform RPM data and send it back to SignalK."""
    # Get the fuel consumption rate at the given RPM
    fuel_rate = fuel.to_m3_per_s(fuel.get_usage(rpm))

    # Calculate torque and power at the given RPM
    torque_value = torque.get_ratio(rpm)
    power_value = power.get_power(rpm)

    # Calculate remaining runTime based on fuel in the tank and fuel consumption rate
    fuel_runtime = utils.get_fuel_runtime(fuel_in_tank, fuel_rate)

    # Bundle all transformed data in a single delta message
    delta_message = {
        "context": "vessels.self",
        "updates": [
            {
                "source": {"label": "drama-python", "type": "python"},
                "timestamp": get_timestamp(),
                "values": [
                    {
                        "path": config["paths"]["fuel"]["path"],
                        "value": fuel_rate,
                        "meta": config["paths"]["fuel"]["meta"],
                    },
                    {
                        "path": config["paths"]["torque"]["path"],
                        "value": torque_value,
                        "meta": config["paths"]["torque"]["meta"],
                    },
                    {
                        "path": config["paths"]["power"]["path"],
                        "value": power_value,
                        "meta": config["paths"]["power"]["meta"],
                    },
                    {
                        "path": config["paths"]["fuel_run_time"]["path"],
                        "value": fuel_runtime,
                    },
                ],
            }
        ],
    }

    # Convert the delta message to a JSON string
    delta_json = json.dumps(delta_message)

    # Send the delta message using the existing WebSocket connection
    print(f"Sending transformed values to SignalK: {delta_json}")
    await websocket.send(delta_json)

    # Calculate BSFC and efficiency and print them (no need to send to SignalK in this case)
    bsfc = utils.calculate_bsfc(fuel.get_usage(rpm), power_value)
    print(f"BSFC at {rpm} RPM: {bsfc} grams per HP per hour")

    efficiency = utils.calculate_efficiency(torque_value, fuel.get_usage(rpm))
    print(f"Efficiency at {rpm} RPM: {efficiency} kg-m per gram")

    # Comparison to factory settings
    comparison = utils.compare_to_factory(rpm, fuel_rate, torque_value, power_value)
    print(f"Comparison at {rpm} RPM: {comparison}")


async def main():
    """Run the receive and send WebSocket connections in parallel."""
    try:
        # Run receive data with a timeout of, for example, 8 minutes (480 seconds)
        await asyncio.wait_for(receive_data(), timeout=480)
    except asyncio.TimeoutError:
        print("WebSocket connection timed out.")


if __name__ == "__main__":
    # Start the event loop and run the WebSockets
    asyncio.get_event_loop().run_until_complete(main())
