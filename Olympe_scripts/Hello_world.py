import olympe
from olympe.messages.ardrone3.Piloting import TakeOff

drone = olympe.Drone("192.168.42.56")
drone.connection()
drone(TakeOff()).wait()
drone.disconnection()
