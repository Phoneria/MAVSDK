#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk import mission_raw


async def px4_connect_drone():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            return drone


async def run():
    drone = await px4_connect_drone()
    await run_drone(drone)


async def run_drone(drone):

    mission_items = []

    mission_items.append(mission_raw.MissionItem(
         0,  # start seq at 0
         6,
         16,
         1,  # first one is current
         1,
         0, 10, 0, float('nan'),
         int(39.87224969075302 * 10**7),
         int(32.73239576154393 * 10**7),
         10.0,
         0
     ))

    mission_items.append(mission_raw.MissionItem(
        1,
        6,
        16,
        0,
        1,
        0, 10, 0, float('nan'),
        int(39.87229815903699 * 10**7),
        int(32.73219051469294 * 10**7),
        10.0,
        0
    ))

    print("-- Uploading mission")
    await drone.mission_raw.upload_mission(mission_items)
    print("-- Done")


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
