import math

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged

with olympe.Drone("10.202.0.1", loglevel=3) as drone:
    drone.connection()
    print("\n\n\n ---------- \n\n\n")

    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()

    print("\n\n\n -----TakeOff complete----- \n\n\n")

    STEPS = 10
    for i in range(STEPS):
        drone(
            moveBy(1, 0, 0, (2*math.pi)/STEPS)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait()

    print("\n\n\n ---- Circle finished ---- \n\n\n")

    drone(
        Landing()
    ).wait()

    print("\n\n\n ---- Drone landed ---- \n\n\n")

    #Leaving the with statement and disconnecting the drone.
