#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

async def go(my_system_address, my_lat, my_long):
    drone = System()
    await drone.connect(system_address=my_system_address)

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)
    # To fly drone 20m above the ground plane
    flying_alt = absolute_altitude + 20.0
    # goto_location() takes Absolute MSL altitude
    await drone.action.goto_location(my_lat, my_long, flying_alt, 0)

    await asyncio.sleep(15)

    print("-- RTL")
    await drone.action.return_to_launch()


if __name__ == "__main__":
    my_lat = 47.398036222362471
    my_long = 8.5450146439425509
    if len(sys.argv)!= 2 :
        #"udp://:14540"
        my_system_address = "serial:///dev/ttyACM0"
        print(f"my_system_address  = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")

    else:
        my_system_address = sys.argv[1]
        my_lat = 39.87236
        my_long = 32.73220
        print(f"my_system_address  = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")


    # Run the asyncio loop
    asyncio.run(go(my_system_address, my_lat, my_long))