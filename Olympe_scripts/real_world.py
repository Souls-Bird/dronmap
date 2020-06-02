import time
import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged

with olympe.Drone("192.168.42.1", loglevel=7) as drone:
    drone.connection()
    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()
    time.sleep(10)
    drone(
        Landing()
    ).wait()

    #implicit disconnection while leaving the with statement.
