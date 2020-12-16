import json
from math import sqrt, acos, pi, cos, sin, radians

class Snowblower:
    def __init__(self, snowzones, heading):
        self.snowzones = snowzones[0]
        self.heading = heading
        # arrays holding distances and angles to try in update method
        self.angles = [120, 60, 90, 150, 30, 180, 0]
        self.distances = [0.25, 1, 2, 3, 4, 5]
        self.max_distance = 5
        self.angle = 90
        self.distance = 1

    # Returns the angle of the snowblower chute
    def get_angle(self, position):
        return self.angle

    # Returns the distance of the snowblower chute
    def get_distance(self, position):
        return self.distance

    # Updates the snowblower chute distance and angle given:
    # robot position, robot heading, and the points traversed.
    # works by converting the cylindral coordinates of the angle and distance to cartesian coordinates, 
    # then checks those coordinates on snowzones and points traversed.
    def update(self, points_traversed, heading, position, robot_width):
    # This first section checks the current distance and angle to test if they are still good.
        previous_x = self.distance * cos(radians(self.angle + (heading - 90)))
        previous_y = self.distance * sin(radians(self.angle + (heading - 90)))
        previous_x2 = self.distance * cos(radians(self.angle + (heading - 90))) + position[0]
        previous_y2 = self.distance * sin(radians(self.angle + (heading - 90))) + position[1]
        if previous_x2 > self.snowzones[0][0] and previous_x2 < self.snowzones[3][0] and previous_y2 > self.snowzones[0][1] and previous_y2 < self.snowzones[3][1]:
            return
        for point in points_traversed:
            x_diff = abs(position[0] - point[0])
            y_diff = abs(position[1] - point[1])
            if x_diff > self.max_distance or y_diff > self.max_distance:
                continue
            x_diff = abs(previous_x - point[0])
            y_diff = abs(previous_y - point[1])
            temp_distance = 1
            temp_angle = 90
            if x_diff <= robot_width/2 and y_diff <= robot_width/2 or previous_x < 0 or previous_y < 0:
                temp_distance = None
                temp_angle = None
                break
            if temp_distance != None:
                return
        # this part looks at all the distances and angles and returns the first one that results in snow being thrown in a snowzone or on uncleared snow.
        for angle in self.angles:
            for distance in self.distances:
                x = distance * cos(radians(angle + (heading - 90)))
                y = distance * sin(radians(angle + (heading - 90)))
                x2 = distance * cos(radians(angle + (heading - 90))) + position[0]
                y2 = distance * sin(radians(angle + (heading - 90))) + position[1]
                if x2 > self.snowzones[0][0] and x2 < self.snowzones[3][0] and y2 > self.snowzones[0][1] and y2 < self.snowzones[3][1]:
                    self.angle = angle
                    self.distance = distance
                    return
                temp_angle = 90
                temp_distance = 1
                for point in points_traversed:
                    x_diff = abs(position[0] - point[0])
                    y_diff = abs(position[1] - point[1])
                    if x_diff > self.max_distance or y_diff > self.max_distance:
                        continue
                    x_diff = abs(x - point[0])
                    y_diff = abs(y - point[1])
                    if x_diff <= robot_width/2 and y_diff <= robot_width/2 or x < 0 or y < 0:
                        temp_distance = None
                        temp_angle = None
                        break
                if temp_distance != None:
                    self.angle = angle
                    self.distance = distance
                    return 
        # If neither snow or snowzones are near, resort to just throwing directly infront of the snowblower.
        self.angle = 90
        self.distance = 1

