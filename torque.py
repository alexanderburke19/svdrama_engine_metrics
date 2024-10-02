import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# RPM and torque data from Yanmar 4JH2E engine service manual
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
        3500,
        3600,
    ]
)

torque = np.array(
    [
        9.75,
        10,
        10.35,
        10.5,
        10.75,
        10.85,
        10.95,
        11,
        11.1,
        11,
        10.99,
        10.95,
        10.9,
        10.8,
        10.35,
        10.2,
        10,
    ]
)

# Torque coefficients
torque_coefficients = [3.67380721e-01, 7.83784240e-03, -1.43743106e-06]
# Create the torque polynomial using the known coefficients
torque_poly = Polynomial(torque_coefficients)
# max torque to calculate torque ratio
max_torque = 11.1


def get_torque(RPM) -> float:
    # returns torque in kg-m at a given RPM
    return torque_poly(RPM)


# Function to calculate torque ratio based on the polynomial and max torque
def get_ratio(rpm, max_torque=11.1):
    # Calculate torque at the given RPM using the polynomial
    torque_at_rpm = torque_poly(rpm)

    # Calculate the torque ratio (0 <= ratio <= 1)
    torque_ratio = torque_at_rpm / max_torque
    return torque_ratio


def get_poly(x, y):
    # Fit a 2nd degree polynomial to the data
    torque_poly = Polynomial.fit(x, y, 2)
    return torque_poly


def get_coefficients(x, y):
    # Fit a 2nd degree polynomial to the data
    torque_poly = Polynomial.fit(x, y, 2)
    return torque_poly.convert().coef
