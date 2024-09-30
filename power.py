import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# RPM data (common for both torque and power)
rpm = np.array(
    [
        1800,
        1900,
        2000,
        2100,
        2200,
        2300,
        2400,
        2500,
        2600,
        2700,
        2800,
        2900,
        3000,
        3200,
        3400,
        3600,
    ]
)

# Propeller power data (HP)
power = np.array(
    [6, 7.5, 8.25, 9.75, 11, 12.5, 14, 16, 17.75, 20, 22.5, 27.5, 33.25, 40, 48]
)

# Propeller power coefficients
power_coefficients = [4.91408457e01, -4.96527228e-02, 1.45559415e-05]
# Create the propeller power polynomial using the known coefficients
power_poly = Polynomial(power_coefficients)


def get_path():
    return "propulsion.main.power"


def get_metadata():
    metadata = {
        "units": "HP",  # Horespower
        "displayName": "Propeller Power",
        "description": "Propeller power in HP",
        "timeout": 60,  # Set a timeout for how long this data is valid (optional)
    }
    return metadata


def get_power(RPM) -> float:
    # returns power in HP at a given RPM
    return power_poly(RPM)


def get_graph(x, y):
    # Generate a smooth curve for plotting
    rpm_smooth = np.linspace(rpm.min(), rpm.max(), 500)
    power_smooth = power_poly(rpm_smooth)
    return power_smooth  # Generate smooth power data over 500 points


def get_chart(rpm, power, rpm_smooth, power_smooth):
    # Plot the original data points and the fitted curve
    plt.figure(figsize=(8, 6))
    plt.plot(rpm[: len(power)], power, "o", label="Propeller Power Data (HP)")
    plt.plot(rpm_smooth, power_smooth, "-", label="Fitted Power Curve")
    plt.title("Propeller Power vs RPM")
    plt.xlabel("RPM")
    plt.ylabel("Power (HP)")
    plt.legend()
    plt.grid(True)
    plt.show()
