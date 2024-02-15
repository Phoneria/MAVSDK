import asyncio
from mavsdk import System
from mavsdk.action import OrbitYawBehavior
import my_connection
import time 
import signal
from mavsdk.mission import (MissionItem, MissionPlan)

target_altitude = 5.0
speed = 5.0
coordinates_x  = [47.398084478529086, 47.3981343499083,47.39782671584852, 47.397750099999996]
coordinates_y  = [8.54591090831239, 8.545277014929143, 8.545181069605313, 8.5456095]

async def go():

    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    mission_items = []
    for i  in range(len(coordinates_x)):
        mission_items.append(MissionItem(coordinates_x[i] ,
                                     coordinates_y[i],
                                     target_altitude,
                                     speed,
                                     True,
                                     float('nan'),
                                     float('nan'),
                                     MissionItem.CameraAction.NONE,
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan'),
                                     float('nan')))
    

    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    first_tour = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    print("UPLOADING MISSION")
    await drone.mission.upload_mission(first_tour)

    print("ARMING")
    await drone.action.arm()

    print("STARTING FIRST TOUR")
    await drone.mission.start_mission()

    await termination_task





async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(f"Mission progress: "
              f"{mission_progress.current}/"
              f"{mission_progress.total}")


async def observe_is_in_air(drone, running_tasks):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return



class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("FUNCTION EXECUTION TIMEOUT")


if __name__ == "__main__":
    # Check if connection takes longer than connection_time second
    connection_time = 30
    signal.signal(signal.SIGALRM, timeout_handler
    signal.alarm(connection_time)  # Set the alarm for connection_time seconds
    try:
        #time.sleep(5)
        asyncio.run(my_connection.main())    
    except TimeoutError:
        print(f"Function took longer than {connection_time} seconds to execute")
        exit()
    finally:
        signal.alarm(0)  # Cancel the alarm
    
    asyncio.run(go())D