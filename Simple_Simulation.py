import os, sys
import pygame
from math import sin, cos, tan, radians, degrees, copysign, acos, atan, sqrt, pi, floor
from pygame.math import Vector2
from pygame.locals import*
from snowblower import*

DT = 0.06


#             R    G    B
PURPLE    = (106,  13, 173)
ORANGE    = (255, 165,   0)
DARKORANGE= (205, 115,   0)
WHITE     = (255, 255, 255)
YELLOW    = (255, 255,   0)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Robot Simulation")
        width = 1000
        height = 1000
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        car_image = pygame.image.load(image_path)
 
        start = [10,10]
        heading = 0.0
        velocity = 5.0
        snowblowerRobot = snowblower(x = start[0], y = start[1], heading=heading, velocity=velocity)
        snowblowerRobot.drive_straight(distance_mm=distance_mm(10))


        ppu = 10

        while not self.exit:
            dt = DT

            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit = True



            # Drawing
            self.screen.fill((0, 0, 0))

            # draw the holonomic robot in its updated location
            # self.draw(snowblowerRobot.position)

            # scale car sprite
            size = car_image.get_size()
            smaller_car = pygame.transform.scale(car_image, (int(size[0]/2), int(size[1]/2)))

            # draw non-holonomic car at the correct angle
            rotated = pygame.transform.rotate(smaller_car, snowblowerRobot.heading)

            rect = rotated.get_rect()
            self.screen.blit(rotated, snowblowerRobot.position * ppu - (rect.width / 2, rect.height / 2))
            pygame.display.flip()

            self.clock.tick(self.ticks)
        self.showGameOverScreen()
        pygame.quit()

    def drawGoal(self, coord):
        x = (coord['x']) * 10
        y = (coord['y']) * 10
        poisonRect = pygame.Rect(x, y, 20, 20) # Rect(left, top, width, height)
        pygame.draw.rect(self.screen, PURPLE, poisonRect)

    def draw(self, coord):
        x = coord.getX() * 10
        y = coord.getY() * 10
        robotSegmentRect = pygame.Rect(x, y, 20, 20)
        pygame.draw.rect(self.screen, DARKORANGE, robotSegmentRect)
        robotInnerSegmentRect = pygame.Rect(x + 4, y + 4, 12, 12)
        pygame.draw.rect(self.screen, ORANGE, robotInnerSegmentRect) 

    def showGameOverScreen(self):
        gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
        gameSurf = gameOverFont.render('Game', True, WHITE)
        overSurf = gameOverFont.render('Over', True, WHITE)
        gameRect = gameSurf.get_rect()
        overRect = overSurf.get_rect()
        gameRect.midtop = (floor(1000 / 2), 10)
        overRect.midtop = (floor(1000 / 2), gameRect.height + 10 + 25)

        self.screen.blit(gameSurf, gameRect)
        self.screen.blit(overSurf, overRect)
        self.drawPressKeyMsg()
        pygame.display.update()
        pygame.time.wait(500)
        self.checkForKeyPress() # clear out any key presses in the event queue

        while True:
            if self.checkForKeyPress():
                pygame.event.get() # clear event queue
                return

    def drawPressKeyMsg(self):
        pressKeySurf = self.BASICFONT.render('Press a key to play.', True, YELLOW)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (1000 - 200, 1000 - 30)
        self.screen.blit(pressKeySurf, pressKeyRect)
    def checkForKeyPress(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.terminate()
        return keyUpEvents[0].key

    def terminate(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()