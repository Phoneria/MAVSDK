#!/usr/bin/env python3

import asyncio
from mavsdk import System
import time 
import signal


async def connect_to_drone(drone):
    await drone.connect(system_address="udp://:14540")
    
    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            time.sleep(0.1)
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("GLOBAL POSITION ESTIMATE IS OKEY")
            time.sleep(0.1)
            break

    print(await drone.telemetry.position().__aiter__().__anext__())
    async for battery in drone.telemetry.battery():
        print(f"BATTERY: {battery.remaining_percent}")
        time.sleep(0.1)

        break

    async for gps_info in drone.telemetry.gps_info():
        print(f"GPS INFO: {gps_info}")
        time.sleep(0.1)

        break

    async for in_air in drone.telemetry.in_air():
        print(f"IN AIR: {in_air}")
        time.sleep(0.1)

        break

    async for flight_mode in drone.telemetry.flight_mode():
        print(f"FLIGHT MODE: {flight_mode}")
        time.sleep(0.1)
        break

    async for health in drone.telemetry.health():
        print(health)
        time.sleep(0.1)
        break


    
async def main():
    drone = System()
    await connect_to_drone(drone)

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("FUNCTION EXECUTION TIMEOUT")


if __name__ == "__main__":
    # Check if connection takes longer than connection_time second
    connection_time = 30
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(connection_time)  # Set the alarm for connection_time seconds
    try:
        #time.sleep(5)
        asyncio.run(main())    
    except TimeoutError:
        print(f"Function took longer than {connection_time} seconds to execute")
        exit()
    finally:
        signal.alarm(0)  # Cancel the alarm
    
    