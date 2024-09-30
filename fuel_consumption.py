import numpy as np
from numpy.polynomial import Polynomial


def get_path():
    """The Signalk path for fuel consumption. Path 'propulsion.main.fuel.rate'.

    Returns:
        string: The Signalk path for fuel consumption.
    """
    return "propulsion.main.fuel.rate"


def get_metadata():
    """Metadata for the Signalk path for fuel consumption. Path 'propulsion.main.fuel.rate'.

    Returns:
        string: A JSON object with metadata for the fuel consumption path.
    """
    metadata = {
        "units": "m3/s",  # Cubic meters per second
        "displayName": "Fuel Consumption",
        "description": "The rate of fuel consumption in cubic meters per second",
        "timeout": 60,  # Set a timeout for how long this data is valid (optional)
    }
    return metadata


def get_usage(RPM) -> float:
    """Calculate fuel consumption at a given RPM using a polynomial derived from engine data in the Yanmar 4JH2E service manual.

    Args:
        RPM (float): The engine speed value from the tachometer

    Returns:
        float: Grams per IIP * hour fuel consumption at the given RPM value
        unit: grams per IIP * hour
    """
    # RPM = engine speed value from tachometer
    # returns grams per IIP * hour
    return fuel_poly(RPM)


def to_liters_per_hour(fuel) -> float:
    """Convert fuel consumption from grams per hour to liters per hour.

    Args:
        fuel (float): Grams per IIP * hour fuel consumption

    Returns:
        float: Liters of consumption per hour at the given fuel rate derived from an RPM value
        unit: liters per hour
    """
    # fuel = grams per IIP * hour
    # returns liters per IIP * hour
    return fuel / 832  # 832 grams per liter


def to_liters_per_minute(fuel) -> float:
    """Convert fuel consumption from grams per hour to liters per minute.

    Args:
        fuel (float): Grams per IIP * hour fuel consumption

    Returns:
        float: Liters of consumption per minute at the given fuel rate derived from an RPM value
        unit: liters per minute
    """
    # fuel = grams per IIP * hour
    # returns liters per hour
    return fuel / 832 / 60  # 60 minutes per hour


def to_gallons_per_hour(fuel) -> float:
    # fuel = grams per IIP * hour
    # returns gallons per IIP * hour
    """Convert fuel consumption from grams per hour to gallons per hour.

    Args:
        fuel (float): Grams per IIP * hour fuel consumption

    Returns:
        float: Gallons of consumption per hour at the given fuel rate derived from an RPM value.
    """
    return fuel / 832 / 3.78541  # 832 grams per liter, 3.78541 liters per gallon


def to_gallons_per_minute(fuel) -> float:
    """Fuel consumption of Gallons per minute derived from an RPM value.

    Args:
        fuel (float): Grams per IIP * hour fuel consumption

    Returns:
        float: Gallons of consumption per minute at the given fuel rate derived from an RPM value
    """
    # fuel = grams per IIP * hour
    # returns gallons per hour
    return fuel / 832 / 3.78541 / 60  # 60 minutes per hour


def to_m3_per_s(fuel) -> float:
    # Convert grams per hour to cubic meters per second
    """Convert fuel consumption from grams per hour to cubic meters per second.
    Default Signalk unit for fuel consumption. Path propulsion.main.fuel.rate

    Args:
        fuel (float): Grams per IIP * hour fuel consumption

    Returns:
        float: Fuel consumption in cubic meters per second at the given fuel rate derived from an RPM value
    """
    flow_rate_m3_per_s = fuel / 2995200
    return flow_rate_m3_per_s


# RPM and fuel consumption data from Yanmar 4JH2E engine service manual
rpm_arr = np.array(
    [1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2800, 3000, 3200, 3400, 3600]
)
fuel_consumption = np.array(
    [250, 238, 227, 219, 212, 205, 200, 196, 188, 187, 183, 182, 184]
)
# Fuel consumption coefficients derived from the data above using numpy's Polynomial.fit() method
fuel_coefficients = [567.487843, -0.239011810, 0.0000369656244]

# The Yanmar 4HJ2E's fuel consumption polynomial using the above coefficients. This is used to calculate fuel consumption at a given RPM. See get_usage() function.
fuel_poly = Polynomial(fuel_coefficients)


def get_poly(x, y):
    # Fit a 2nd degree polynomial to the data
    fuel_poly = Polynomial.fit(x, y, 2)
    return fuel_poly


def get_coefficients(x, y):
    # Fit a 2nd degree polynomial to the data
    fuel_poly = Polynomial.fit(x, y, 2)
    return fuel_poly.convert().coef


def get_curve(rpm_arr, fuel_poly):
    # Generate a smooth curve for plotting
    rpm_smooth = np.linspace(rpm_arr.min(), rpm_arr.max(), 500)
    fuel_smooth = fuel_poly(rpm_smooth)
    return fuel_smooth
