import asyncio

from mavsdk import System


async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    mission_import_data = await drone.mission_raw.import_qgroundcontrol_mission(
        "example_mission.plan"
    )
    print(f"{len(mission_import_data.mission_items)} mission items imported")
    await drone.mission_raw.upload_mission(mission_import_data.mission_items)
    print("Mission uploaded")

    await drone.action.arm()
    await drone.mission.start_mission()


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
