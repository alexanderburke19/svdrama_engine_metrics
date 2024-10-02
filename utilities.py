from fuel_consumption import fuel_poly
from torque import torque_poly
from power import power_poly


# Function to calculate runtime based on fuel in the tank and fuel consumption rate
def get_fuel_runtime(fuel_in_tank_liters, fuel_consumption_rate_g_per_h):
    """Calculate the runtime based on the fuel in the tank and the fuel consumption rate

    Args:
        fuel_in_tank_liters (float): The amount of fuel in the tank in liters
        fuel_consumption_rate_g_per_h (float): The fuel consumption rate in grams per hour based on current RPM

    Returns:
        float: The amount of time the engine can run based on the fuel in the tank and the fuel consumption rate at a given RPM
    """
    # Convert fuel in the tank to grams
    fuel_in_tank_grams = fuel_in_tank_liters * 832  # 832 grams per liter for diesel

    # Calculate runtime in hours
    runtime_hours = fuel_in_tank_grams / fuel_consumption_rate_g_per_h

    # Convert runtime to minutes
    runtime_minutes = runtime_hours * 60

    # Convert runtime to seconds
    runtime_seconds = runtime_minutes * 60
    return runtime_seconds


# Define a function to calculate BSFC (Brake Specific Fuel Consumption)
def calculate_bsfc(fuel_consumption, power):
    return fuel_consumption / power


# Define a function to calculate an efficiency score (Torque-to-Fuel ratio)
def calculate_efficiency(torque, fuel_consumption):
    return torque / fuel_consumption


# Function to compare real-time data to factory data
def compare_to_factory(rpm, real_fuel, real_torque, real_power):
    # Calculate expected values using factory data polynomials
    expected_fuel = fuel_poly(rpm)
    expected_torque = torque_poly(rpm)
    expected_power = power_poly(rpm)

    # Calculate deviations (in percentage)
    fuel_deviation = (real_fuel - expected_fuel) / expected_fuel * 100
    torque_deviation = (real_torque - expected_torque) / expected_torque * 100
    power_deviation = (real_power - expected_power) / expected_power * 100

    return fuel_deviation, torque_deviation, power_deviation


# Function to calculate total power output including alternator power
def calculate_total_power(rpm, alternator_output_watts):
    # Calculate propeller power from your polynomial (convert HP to W)
    mechanical_power_watts = power_poly(rpm) * 745.7

    # Total power = mechanical (propeller) power + electrical power (from alternator)
    total_power_watts = mechanical_power_watts + alternator_output_watts

    return total_power_watts


# Function to calculate overall fuel efficiency
def calculate_fuel_efficiency(rpm, alternator_output_watts, real_fuel_consumption):
    # Calculate total power output
    total_power_watts = calculate_total_power(rpm, alternator_output_watts)

    # Calculate efficiency (W per gram of fuel)
    efficiency = total_power_watts / real_fuel_consumption

    return efficiency
