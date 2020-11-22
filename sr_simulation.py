import os
import sys
import pygame
from math import sin, cos, tan, radians, degrees, copysign, acos, atan, sqrt, pi, floor
from pygame.math import Vector2
from pygame.locals import*
from Snowblower import*
from Robot import*
from CoverageAlgorithm import*

DT = 0.06


#             R    G    B
PURPLE = (106,  13, 173)
ORANGE = (255, 165,   0)
DARKORANGE = (205, 115,   0)
WHITE = (255, 255, 255)
YELLOW = (255, 255,   0)
BLACK = (0, 0,   0)

CELLSIZE = 1
ROBOT_WIDTH = 10


def drawPoint(screen, x, y, color):
    pointRect = pygame.Rect(int(x), int(y), CELLSIZE, CELLSIZE)
    pygame.draw.rect(screen, color, pointRect)


class SnowRemovalSim:
    def __init__(self, parkinglot, snowzones, robotInit):
        pygame.init()
        pygame.display.set_caption("Snow Removal")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        self.parkinglot = parkinglot
        self.snowzones = snowzones
        self.robot = Robot(
            robotInit['origin'][0], robotInit['origin'][1], robotInit['heading'], DT)
        self.snowblower = Snowblower(snowzones, 0)
        self.points_traversed = []

    def drawPointsTraversed(self):
        for point in self.points_traversed:
            drawPoint(self.screen, point[0], point[1], PURPLE)

    def addCoveragePoints(self, current_position):
        # assume that the robot position indicates the front-center of the robot
        self.points_traversed.append(current_position)
        iterateNum = int(ROBOT_WIDTH / 2)
        while iterateNum < 0:  # robot.width / 2:
            # handle left side
            leftAngle = self.robot.heading + 90
            leftPos = self.robot.position
            leftPos[0] += leftPos[0]*cos(leftAngle)
            leftPos[1] += leftPos[1]*sin(leftAngle)
            self.points_traversed.append([leftPos[0], leftPos[1]])

            # handle right side
            rightAngle = self.robot.heading - 90
            rightPos = self.robot.position
            rightPos[0] -= rightPos[0]*cos(rightAngle)
            rightPos[1] -= rightPos[1]*sin(rightAngle)
            self.points_traversed.append([rightPos[0], rightPos[1]])
            iterateNum = iterateNum - 1

    def drawRobot(self, position, direction):
        # todo
        drawPoint(self.screen, position[0], position[1], DARKORANGE)
        return

    def drawBlower(self, angle, distance):
        # todo
        return

    def run(self):
        # build instructions with coverage algorithm
        covAlg = CoverageAlgorithm(self.parkinglot)
        instructions = covAlg.getInstructions()

        while not self.exit:
            dt = self.clock.get_time() / 1000

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            # # User input
            # pressed = pygame.key.get_pressed()

            list_of_points = []
            # Logic
            for i in range(0, len(instructions)):
                angle = instructions[i][0]
                if angle != self.robot.heading:
                    self.robot.turn_in_place(angle)
                distance = instructions[i][1]
                list_of_points = self.robot.drive_straight(distance)

                for j in range(0, len(list_of_points)):
                    current_position = list_of_points[j]
                    blower_angle = self.snowblower.get_direction(
                        current_position)
                    blower_distance = self.snowblower.get_pitch(
                        current_position)

                    # erase the screen
                    self.screen.fill(BLACK)

                    # draw the points traversed
                    self.addCoveragePoints(current_position)
                    self.drawPointsTraversed()

                    # draw the robot
                    self.drawRobot(current_position, self.robot.heading)

                    # draw the snowblower
                    self.drawBlower(blower_angle, blower_distance)

                    pygame.display.flip()
                    self.clock.tick(self.ticks)

        pygame.quit()


def getFile(argv):
    # determine the json file
    n = len(sys.argv)
    if n == 1:
        print("Please specify JSON config filename")
        return None
    filename = sys.argv[1]
    try:
        with open(filename) as f:
            data = json.load(f)
        return data
    except:
        print("Unable to access file")
        return None


if __name__ == '__main__':
    # load the parking lot
    initState = getFile(sys.argv[1:])
    if initState is not None:
        print(initState)
        srSim = SnowRemovalSim(initState['parkingLot']['outline'],
                               initState['parkingLot']['snowZones'], initState['robot'])
        srSim.run()
