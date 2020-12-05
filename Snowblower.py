import json
from math import sqrt, acos, pi, cos, sin

# TODO


class Snowblower:
    def __init__(self, snowzones, heading):
        self.snowzones = snowzones
        self.heading = heading
        self.angles = [180, 150, 120, 90, 60, 30, 0]
        self.left_angle = 180
        self.right_angle = 0
        self.max_distance = 5
        self.previous_angle = 90
        self.previous_distance = 1
        self.angle = 0
        self.distance = 1

    def get_angle(self, position):
        # TODO
        angle = 0
        return -90
        #return self.angle

    def get_distance(self, position):
        # TODO
        distance = 1
        return 2
        #return self.distance

    def update(self, points_traversed, heading, position, robot_width):
        previous_x = int(self.distance * cos(self.angle + (90 - heading)) + position[0])
        previous_y = int(self.distance * sin(self.angle + (90 - heading)) + position[1])
        print(self.snowzones)
        print(f" 1: {self.snowzones[0]}, 2: {self.snowzones[3]}, 3: {self.snowzones[0]}, 4: {self.snowzones[3]}")
        if previous_x > self.snowzones[0][0] and previous_x < self.snowzones[3][0] and previous_y > self.snowzones[0][1] and previous_y < self.snowzones[3][1]:
            self.angle = angle
            self.distance = distance
            return
        for point in points_traversed:
            x_diff = abs(position[0] - point[0])
            y_diff = abs(position[1] - point[1])
            if x_diff > self.max_distance or y_diff > self.max_distance:
                continue
            x_diff = abs(previous_x - point[0])
            y_diff = abs(previous_y - point[1])
            if x_diff <= robot_width/2 and y_diff <= robot_width/2:
                temp_distance = None
                temp_angle = None
                break
            if temp_distance != None:
                self.angle = angle
                self.distance = distance
                return
        for angle in self.angles:
            for distance in range(1,6):
                x = distance * cos(angle + (90 - heading)) + position[0]
                y = distance * sin(angle + (90 - heading)) + position[1]
                if x > self.snowzones[0][0] and x < self.snowzones[3][0] and y > self.snowzones[0][1] and y < self.snowzones[3][1]:
                    self.angle = angle
                    self.distance = distance
                    return
                temp_angle = 0
                temp_distance = 1
                for point in points_traversed:
                    x_diff = abs(position[0] - point[0])
                    y_diff = abs(position[1] - point[1])
                    if x_diff > self.max_distance or y_diff > self.max_distance:
                        continue
                    x_diff = abs(x - point[0])
                    y_diff = abs(y - point[1])
                    if x_diff <= robot_width/2 and y_diff <= robot_width/2:
                        temp_distance = None
                        temp_angle = None
                        break
                if temp_distance != None:
                    self.angle = angle
                    self.distance = distance
                    return 

