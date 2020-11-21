import json
from math import sqrt, acos, pi, cos, sin


class Robot:
    def __init__(self, x = 0.0, y = 0.0, heading = 0, velocity = 0.0):
        self.heading = heading
        self.position = [x, y]
        self.velocity = velocity

    def drive_straight(self, distance_mm = 0.0, speed_mmps = 0.0):
        self.velocity = speed_mmps

        list_of_points_to_traverse = []

        for x in range(0, distance_mm):
            list_of_points_to_traverse.append(
                [x*cos(self.heading), x*sin(self.heading)])

        return list_of_points_to_traverse

    def turn_in_place(self, degrees=0.0):
        # TODO: Simulate turning
        self.heading += degrees

    def distance_mm(self, dist):
        return dist

    def speed_mmps(self, speed):
        return speed

    def degrees(self, angle):
        return angle


"""
    # drive in a straight line 100 mm at a speed of 30 mm/s
    robot.behavior.drive_straight(distance_mm(100), speed_mmps(30))

    # turn the robot 90 degrees
    robot.behavior.turn_in_place(degrees(90))
"""
