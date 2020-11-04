import json
from math import sqrt, acos, pi

class Vector:
    def __init__(self, i = 0.0, j = 0.0):
        i = float(i)
        j = float(j)

class Position:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def getX(self):
        return self.x

    def getY(self):
        return self.y

class snowblower:
    def __init__(self, x = 0.0, y = 0.0, heading = 0.0, velocity = 0.0):
        self.heading = heading
        self.position = Position(x, y)
        self.velocity = velocity

        self.fullyCoveredBool = False

    def drive_straight(self, distance_mm = 0.0, speed_mmps = 0.0):
        pass

    def turn_in_place(self, degrees = 0.0):
        pass

"""
    # drive in a straight line 100 mm at a speed of 30 mm/s
    robot.behavior.drive_straight(distance_mm(100), speed_mmps(30))

    # turn the robot 90 degrees
    robot.behavior.turn_in_place(degrees(90))
"""
    
