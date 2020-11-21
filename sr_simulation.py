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
        self.robot = Robot(robotInit.x, robotInit.y,
                           robotInit.angle, robotInit.heading)
        self.snowblower = Snowblower(snowzones, 0)

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

            # Logic
            # TODO move the robot
            # TODO adjust the snow blower

            # copied from the UML doc
            # For i  in range(0, len(instructions)):
            # Angle = instructions[i][0]
            # If Angle != Robot.heading:
            # 	Robot.turn_in_place(Angle)

            # Distance = instructions[i][1]
            # List_of_points = Robot.drive_straight(Distance)

            # For j in range(0, len(list_of_points)):
            # 	Current_position = list_of_points[j]
            # 	Blower_angle = Snowblower.get_direction(current_position)

            # Drawing
            self.screen.fill((0, 0, 0))
            # TODO: display the robot
            # TODO: display the snowblower path
            # TODO: (maybe) display the instructions

            pygame.display.flip()

            self.clock.tick(self.ticks)
        pygame.quit()


def getFile(argv):
    # determine the json file
    n = len(sys.argv)
    if n == 1:
        print("Please specify JSON config filename")
        return
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
    if initState is None:
        exit

    srSim = SnowRemovalSim(initState.parkingLot.outline,
                           initState.parkingLot.snowDumpZones, initState.robot)
    srSim.run()
