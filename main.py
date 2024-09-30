#!/usr/bin/env python3

import numpy as np
import utilities as utils
import ws_deltas as ws
import fuel_consumption as fuel
import torque as torque
import power as power

# rpm value for testing purposes
rpm_value = 2750
# fuel in tank in liters
fuel_in_tank = 100  # in liters


if __name__ == "__main__":

    # Simulate sending values to the WebSocket from main
    for rpm in range(1000, 3000, 500):
        fuel_rate = fuel.to_m3_per_s(fuel.get_usage(rpm))
        print(f"Calculated fuel consumption: {fuel_rate}")
        ws.send_signal_k_delta(fuel.get_path(), fuel_rate, fuel.get_metadata())

        torque_value = torque.get_ratio(rpm)
        print(f"Torque at {rpm_value} RPM: {torque_value} kg-m")
        ws.send_signal_k_delta(torque.get_path(), torque_value, torque.get_metadata())

        power_value = power.get_power(rpm)
        print(f"Power at {rpm_value} RPM: {power_value} HP")
        ws.send_signal_k_delta(power.get_path(), power_value, power.get_metadata())

        bsfc = utils.calculate_bsfc(fuel.get_usage(rpm), power_value)
        print(f"BSFC at {rpm} RPM: {bsfc} grams per HP per hour")

        efficiency = utils.calculate_efficiency(torque_value, fuel.get_usage(rpm))
        print(f"Efficiency at {rpm_value} RPM: {efficiency} kg-m per gram")

        fuel_runtime = utils.get_fuel_runtime(fuel_in_tank, fuel_rate)
        print(f"Fuel runtime: {fuel_runtime} hours")
        ws.send_signal_k_delta("propulsion.main.fuel.runtime", fuel_runtime)

    # comparison = utils.compare_to_factory(
    #    rpm_value, fuel_consumption, torque_value, power_value
    # )
    # print(f"Comparison at {rpm_value} RPM: {comparison}")
