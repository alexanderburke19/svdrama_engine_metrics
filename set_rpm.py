#!/usr/bin/env python3

import numpy as np
import ws_deltas as ws

# rpm value for testing purposes
# Generate a random float between 0 and 3600
random_float = np.random.uniform(1500.0, 3600.0)  # Range is 0 <= random_float < 3600
rpm = random_float  # Random RPM value for testing


if __name__ == "__main__":

    # Send the RPM value to the server
    ws.send_signal_k_delta("propulsion.main.revolutions", rpm)
