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


def get_power(RPM) -> float:
    # returns power in HP at a given RPM
    return power_poly(RPM)
