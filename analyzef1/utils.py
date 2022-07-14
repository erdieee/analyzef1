from typing import List

def get_driver_abbreviation(drivers_dict: dict) -> List:
    drivers = []
    for i in list(drivers_dict.keys()):
        drivers.append(drivers_dict[i]['Abbreviation'])
    return drivers