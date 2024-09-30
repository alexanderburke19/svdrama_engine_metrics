#!/usr/bin/env python3

import numpy as np
import utilities as utils
import ws_deltas as ws
import fuel_consumption as fuel
import torque as torque
import power as power

# rpm value for testing purposes
# Generate a random float between 0 and 3600
random_float = np.random.uniform(0.0, 3600.0)  # Range is 0 <= random_float < 3600
rpm = random_float  # Random RPM value for testing
# fuel in tank in liters
fuel_in_tank = 100  # in liters


if __name__ == "__main__":

    # Send the RPM value to the server
    ws.send_delta("propulsion.main.revolutions", rpm)

    # Get the fuel consumption rate at the given RPM
    fuel_rate = fuel.to_m3_per_s(fuel.get_usage(rpm))
    # Send the path and value to the server: propulsion.main.fuel.rate
    ws.send_signal_k_delta(fuel.get_path(), fuel_rate, fuel.get_metadata())

    # Calculate torque and power at the given RPM
    torque_value = torque.get_ratio(rpm)
    # Send the path and value to the server: propulsion.main.engineTorque
    ws.send_signal_k_delta(torque.get_path(), torque_value, torque.get_metadata())

    # Calculate propeller power at the given RPM
    power_value = power.get_power(rpm)
    # Send the path and value to the server: propulsion.main.power
    ws.send_signal_k_delta(power.get_path(), power_value, power.get_metadata())

    # Calculate remaining runTime based on fuel in the tank and fuel consumption rate
    fuel_runtime = utils.get_fuel_runtime(fuel_in_tank, fuel_rate)
    # Send the path and value to the server: propulsion.main.fuel.runTime
    ws.send_signal_k_delta("propulsion.main.fuel.runTime", fuel_runtime)

    # Calculate BSFC at the given RPM
    bsfc = utils.calculate_bsfc(fuel.get_usage(rpm), power_value)
    print(f"BSFC at {rpm} RPM: {bsfc} grams per HP per hour")

    # Calculate efficiency at the given RPM
    efficiency = utils.calculate_efficiency(torque_value, fuel.get_usage(rpm))
    print(f"Efficiency at {rpm} RPM: {efficiency} kg-m per gram")

    # Implement real comparison to factory settings. Get expected values from factory data. Will equal 100% if values match.
    comparison = utils.compare_to_factory(rpm, fuel_rate, torque_value, power_value)
    print(f"Comparison at {rpm} RPM: {comparison}")
