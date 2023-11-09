import json
from datetime import datetime
from typing import Dict, Any

import messages
from custom_print import PPrint

# Store vehicle objects in-memory
VEHICLE_DB = dict()

# Parking lot capacity
CAPACITY = 20


class Parking:
    """
    A parking class to contain all level with their respected initial spot and capacity
    """

    def __init__(self, level, initial_spot_number):
        self.level = level
        self.initial_spot_number = initial_spot_number
        self.spots_allocated = -1

    def get_available_spot(self) -> int:
        """
        Find the available spot by checking the capacity limit
        :return: integer depicting the available spot or -1 in case there is no spot available
        """

        if (self.spots_allocated + 1) < CAPACITY:
            self.spots_allocated += 1
            return self.initial_spot_number + self.spots_allocated
        return -1


class Vehicle:
    """
    A vehicle class to contain all vehicle related information
    """

    def __init__(self, vehicle_id, level, parking_spot_number):
        self.vehicle_id = vehicle_id
        self.level = level
        self.parking_spot_number = parking_spot_number

    def get_parking_details(self) -> Dict[str, Any]:
        """
        Format details as per requirement:
        {"level": "A", "spot": 19}

        :return: A dict containing parking level and the parking spot number.
        """
        return {
            "level": self.level,
            "spot": self.parking_spot_number
        }


def generate_unique_vehicle_number() -> str:
    """
    Generate vehicle number, Which will be served as a unique vehicle ID.
    :return: A string contain the label and current timestamp
    """

    return f"VHL-{round(datetime.utcnow().timestamp())}"


if __name__ == '__main__':
    # Create parking objects for each level
    A = Parking(level='A', initial_spot_number=1)
    B = Parking(level='B', initial_spot_number=21)

    # Initialize the pprint for printing colorful messages
    pprint = PPrint()

    pprint.print_default(messages.GREET)

    while True:
        pprint.print_default(messages.INPUT_CHOICES)

        choice = input("Waiting... ")

        # Check if the input container any invalid choices
        if choice not in {'1', '2', '0'}:
            pprint.print_error(messages.CHOICE_ERROR)
            continue

        if choice == '1':
            vehicle_number = input("Please enter your vehicle number or press enter/return to auto-generate the "
                                   "vehicle number: ")

            # Generate vehicle number if user didn't provide one
            if not vehicle_number:
                vehicle_number = generate_unique_vehicle_number()

            # Check if vehicle number already exists in the DB or not.
            if VEHICLE_DB.get(vehicle_number):
                pprint.print_error(messages.VEHICLE_ALREADY_ALLOCATED)
                continue

            # Scan the parking level A, If there is any available parking spot
            available_spot = A.get_available_spot()
            parking_level = A.level

            # Scan the parking level B, If there is any available parking spot, In case the there isn't any parking
            # space left on level A
            if available_spot == -1:
                available_spot = B.get_available_spot()
                parking_level = B.level

            # Check if there is any space available or not, After scanning both the parking levels
            if available_spot == -1:
                pprint.print_error(messages.NO_SPOT_AVAILABLE)
                continue

            # Create the vehicle object and store it in the DB
            vehicle = Vehicle(
                vehicle_id=vehicle_number,
                level=parking_level,
                parking_spot_number=available_spot
            )

            VEHICLE_DB[vehicle_number] = vehicle
            pprint.print_success(messages.VEHICLE_ALLOCATED_SUCCESS.format(vehicle_number))

        elif choice == '2':
            vehicle_number = input("Please enter your vehicle number: ")

            # Validate if the input vehicle number is empty or not
            if not vehicle_number:
                pprint.print_error(messages.INVALID_VEHICLE_NUMBER)
                continue

            vehicle = VEHICLE_DB.get(vehicle_number)

            # Check if there is any vehicle record exists in the DB or not.
            if not vehicle:
                pprint.print_error(messages.VEHICLE_DOES_NOT_EXISTS)
                continue

            # Fetch the parking details of the respected vehicle
            result = vehicle.get_parking_details()
            pprint.print_success(json.dumps(result))
            continue
        else:
            pprint.print_default(messages.EXIT)
            break
