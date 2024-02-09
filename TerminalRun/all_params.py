#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

async def run(my_system_address):
    # Connect to the drone
    drone = System()
    await drone.connect(system_address=my_system_address)

    # Get the list of parameters
    all_params = await drone.param.get_all_params()

    # Iterate through all int parameters
    for param in all_params.int_params:
        print(f"{param.name}: {param.value}")

    for param in all_params.float_params:
        print(f"{param.name}: {param.value}")

if __name__ == "__main__":

    if len(sys.argv)!= 2 :
        #"udp://:14540"
        my_system_address = "/dev/ttyAMA0"
        print(f"my_system_address  = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")

    else:
        my_system_address = sys.argv[1]
        print(f"my_system_address  = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")


    # Run the asyncio loop
    asyncio.run(run(my_system_address))
