import math
import time

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing, PCMD
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged

with olympe.Drone("10.202.0.1", loglevel=3) as drone:
    drone.connection()
    print("\n\n\n ---------- \n\n\n")

    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()

    print("\n\n\n -----TakeOff complete----- \n\n\n")

    while True:
        drone(
            PCMD(1, roll=20, pitch=100, yaw=50, gaz=20, timestampAndSeqNum=0)
        ).wait()
        time.sleep(0.2)

    print("\n\n\n ---- Circle finished ---- \n\n\n")

    drone(
        Landing()
    ).wait()

    print("\n\n\n ---- Drone landed ---- \n\n\n")

    #Leaving the with statement and disconnecting the drone.
