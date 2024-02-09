#!/usr/bin/env python3

import asyncio
from mavsdk import System
import sys

async def go(my_system_address):

    drone = System()
    await drone.connect(system_address=my_system_address)

    status_text_task = asyncio.ensure_future(print_status_text(drone))

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()

    status_text_task.cancel()


async def print_status_text(drone):
    try:
        async for status_text in drone.telemetry.status_text():
            print(f"Status: {status_text.type}: {status_text.text}")
    except asyncio.CancelledError:
        return


if __name__ == "__main__":

    if len(sys.argv)!= 2 :
        #"udp://:14540"
        my_system_address = "/dev/ttyAMA0"
        print(f"my_system_address  = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")

    else:
        my_system_address = sys.argv[1]
        print(f"my_system_address = {my_system_address} . \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")


    # Run the asyncio loop
    asyncio.run(go(my_system_address))