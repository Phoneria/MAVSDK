import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
import sys

async def go(my_system_address, my_lat, my_long):
    drone = System()
    await drone.connect(system_address=my_system_address)

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    position = await drone.telemetry.position().__aiter__().__anext__()
    orbit_height = position.absolute_altitude_m+10
    yaw_behavior = OrbitYawBehavior.HOLD_FRONT_TO_CIRCLE_CENTER

    print("-- Arming")
    await drone.action.arm()

    print("--- Taking Off")
    await drone.action.takeoff()
    await asyncio.sleep(10)

    print('Do orbit at 10m height from the ground')
    await drone.action.do_orbit(radius_m=10,
                                velocity_ms=2,
                                yaw_behavior=yaw_behavior,
                                latitude_deg= my_lat,
                                longitude_deg=my_long,
                                absolute_altitude_m=orbit_height)
    await asyncio.sleep(60)

    await drone.action.return_to_launch()
    print("--- Landing")

if __name__ == "__main__":
    my_lat = 47.398036222362471
    my_long = 8.5450146439425509
    if len(sys.argv)!= 2 :
        #"udp://:14540"
        my_system_address = "/dev/ttyAMA0"
        print(f"Total Time = {my_system_address} minute. \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")

    else:
        my_system_address = sys.argv[1]
        my_lat = 39.87209
        my_long = 32.73220
        print(f"Total Time = {my_system_address} minute. \nLET'SSSS GOOOOOOOOOOO!!!!!!!!!")


    # Run the asyncio loop
    asyncio.run(go(my_system_address, my_lat, my_long))