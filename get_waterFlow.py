#!/usr/bin/env python3

import re
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import ws_deltas as ws

# InfluxDB connection details
influx_url = "http://10.10.10.1:8086"  # Replace with your InfluxDB URL if different
token = "_ITpt23iHlg4P25jp7sR_6xtRn3KH3SkH0lKXlPfzWHSrhD1C4aMm6w885GajnYSw1fLb7M9AOt2bNwITVCdaA=="  # Replace with your actual InfluxDB token
org = "drama"  # Replace with your InfluxDB organization
bucket = "drama"  # Replace with your InfluxDB bucket

# InfluxDB client initialization
client = InfluxDBClient(url=influx_url, token=token, org=org)
# Tank capacity
tank_capacity = 100  # liters


# Query for the total value of each path
def query_value(path):
    query = f"""
    from(bucket: "{bucket}")
      |> range(start: 0)
      |> filter(fn: (r) => r["_measurement"] == "{path}")
      |> sum()
    """
    result = client.query_api().query(org=org, query=query)

    value = None
    for table in result:
        for record in table.records:
            value = record.get_value()

    return value


# Calculate total inflow - outflow
def calculate_total(inflow_path, outflow_path, initial_value):
    inflow_value = query_value(inflow_path)
    outflow_value = query_value(outflow_path)

    if inflow_value is not None and outflow_value is not None:
        current_value = initial_value - (inflow_value - outflow_value)
        return (current_value / tank_capacity) * 100  # currentLevel as ratio 0 - 100
    else:
        return None


# Paths for inflow and outflow
paths = {
    "starboard": {
        "initial_value": 50,  # in liters
        "inFlow": "tanks.freshWater.starboard.inFlow",
        "outFlow": "tanks.freshWater.starboard.outFlow",
    },
    "port": {
        "initial_value": 50,  # in liters
        "inFlow": "tanks.freshWater.port.inFlow",
        "outFlow": "tanks.freshWater.port.outFlow",
    },
}

# Calculate total and print the results
for side, path_info in paths.items():
    total_value = calculate_total(
        path_info["inFlow"], path_info["outFlow"], path_info["initial_value"]
    )
    if total_value is not None:
        total_path = f"tanks.freshWater.{side}.currentLevel"
        print(f"Total for {total_path}: {total_value}")
        # Send the total value to SignalK
        ws.send_signal_k_delta(total_path, total_value)
    else:
        print(f"No data available for {side} side")

# Close the client connection
client.close()
