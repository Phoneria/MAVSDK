import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
import my_connection
import time 
import signal


target_altitude = 10

async def takeoff_land():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("DRONE STARTED TO TAKEOFF")

    await drone.action.set_takeoff_altitude(target_altitude)

    print(await drone.telemetry.position().__aiter__().__anext__())

    print("ARMING")
    await drone.action.arm()

    print("TAKING OFF")
    print("TAKEOFF ALTITUDE : ", target_altitude)
    await drone.action.takeoff()

    await asyncio.sleep(target_altitude/2  + 10) #  Wait For takeoff
    
    print(await drone.telemetry.position().__aiter__().__anext__())

    print("TAKEOFF COMPLETED")

    await asyncio.sleep(target_altitude/2  + 10) #  Wait For takeoff

    print("LANDING")
    await drone.action.land()

    await asyncio.sleep(target_altitude/2  + 10) #  Wait For takeoff

    print("TAKEOFF & LAND COMPLETED")

    
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
        asyncio.run(my_connection.main())    
    except TimeoutError:
        print(f"Function took longer than {connection_time} seconds to execute")
        exit()
    finally:
        signal.alarm(0)  # Cancel the alarm
    
    asyncio.run(takeoff_land())