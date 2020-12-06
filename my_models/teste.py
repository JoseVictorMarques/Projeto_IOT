	

# -*- coding: UTF-8 -*-

import olympe
from olympe.messages.ardrone3.Piloting import TakeOff, moveBy, Landing
from olympe.messages.ardrone3.PilotingState import FlyingStateChanged

DRONE_IP = "10.202.0.1"

def main():
    drone = olympe.Drone(DRONE_IP)
    drone.connect()
    drone(
        TakeOff()
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()
    drone(
        moveBy(3, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()
    drone(
        moveBy(0, 4, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()
    drone(
        moveBy(-3, 0, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait()
    drone(
        moveBy(0, -4, 0, 0)
        >> FlyingStateChanged(state="hovering", _timeout=5)
    ).wait().success()
    drone(Landing()).wait()
    drone.disconnect()

if __name__ == "__main__":
	main()
