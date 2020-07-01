import time
import logging

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing, NavigateHome, moveTo
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged, NavigateHomeStateChanged, moveToChanged
from olympe.enums.ardrone3.Piloting import MoveTo_Orientation_mode
from olympe.messages.ardrone3.GPSSettingsState import GPSFixStateChanged, HomeChanged


# olympe.log.set_config(logging.basicConfig(level=logging.DEBUG))

with olympe.Drone("10.202.0.1") as drone:
    drone.connect()
    print("\n\n\n ----- Starting experience ----- \n\n\n")

    drone(GPSFixStateChanged(fixed=1, _timeout=10, _policy='check_wait')).wait()
    drone_home = drone.get_state(HomeChanged)
    print(drone_home)

    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()

    print("\n\n\n -----TakeOff complete----- \n\n\n")


    N_STEPS = 2 #number of steps before back to base
    STEP = 2    #Distance (in m) of one step forward
    for i in range(N_STEPS):
        drone(
            moveBy(STEP, 0, 0, 0)
            >> FlyingStateChanged(state="hovering", _timeout=5)
        ).wait()
        time.sleep(10)

    print("\n\n\n ---- Experience finished, Back to home ---- \n\n\n")

    drone(
        moveTo(drone_home['latitude'], drone_home['longitude'], drone_home['altitude'], MoveTo_Orientation_mode.NONE, 0.0)
        >> moveToChanged(status='DONE')
    ).wait()

    print("\n\n\n ---- Landing... ---- \n\n\n")

    drone(
        Landing()
    ).wait()

    print("\n\n\n ---- Drone landed ---- \n\n\n")

    #Leaving the with statement and disconnecting the drone.
