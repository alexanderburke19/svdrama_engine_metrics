#!/usr/bin/env python3

import numpy as np
import ws_deltas as ws
import yaml


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
sides = ["port", "starboard"]


def set_inFlow():
    """set the inFlow value for testing purposes.
    data will be stored in influxDB for time series analytics.
    ultimitly the data will be used to predict the water level in the tanks."""
    meta = config["paths"]["freshWater_inFlow"]["meta"]
    for i in sides:
        flow = np.random.uniform(0.000, 1.500)
        # Send the flow value to the server
        ws.send_signal_k_delta(f"tanks.freshWater.{i}.inFlow", flow, metadata=meta)


def set_outFlow():
    """set the outFlow value for testing purposes.
    data will be stored in influxDB for time series analytics.
    ultimitly the data will be used to predict the water level in the tanks."""
    meta = config["paths"]["freshWater_outFlow"]["meta"]
    for i in sides:
        flow = np.random.uniform(1.000, 1.500)
        # Send the flow value to the server
        ws.send_signal_k_delta(f"tanks.freshWater.{i}.outFlow", flow, metadata=meta)


def main():
    for rate in range(50):
        set_inFlow()
        set_outFlow()


if __name__ == "__main__":
    for rate in range(50):
        set_inFlow()
        set_outFlow()
