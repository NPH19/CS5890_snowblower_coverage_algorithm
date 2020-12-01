

# {
#   parkingLot :{
#       outline: [[0,0], [0, 100],[100, 100], [100, 0], [0, 0]],
#       snowZone: [[90,0], [90, 100],[100, 100], [100, 0], [90, 0]],
#   },
#   robot { x:0, y:0, heading:90}
MOCK_INSTRUCTIONS = [
    # swath 1
    # go strait
    [0, 100],
    # turn right and reposition for the next swath
    [-90, 10],
    # turn right, then go strait,
    [-90, 100],
    # swath 2
    # turn left and reposition for the next swath
    [90, 10],
    # turn left to reposition for next swath then go strait
    [90, 100],
    # swath 3
    # turn right and reposition for the next swath
    [-90, 10],
    # turn right, then go strait,
    [-90, 100],
    # swath 4
    # turn left and reposition for the next swath
    [90, 10],
    # turn left to reposition for next swath then go strait
    [90, 100],
    # swath 5
    # turn right and reposition for the next swath
    [-90, 10],
    # turn right, then go strait,
    [-90, 100],
    # swath 6
    # turn left and reposition for the next swath
    [90, 10],
    # turn left to reposition for next swath then go strait
    [90, 100],
    # swath 7
    # turn right and reposition for the next swath
    [-90, 10],
    # turn right, then go strait,
    [-90, 100],
    # swath 8
    # turn left and reposition for the next swath
    [90, 10],
    # turn left to reposition for next swath then go strait
    [90, 100],
    # swath 9 (final swath because of the the snow zone)
    # # turn right and reposition for the next swath
    # [-90, 10],
    # # turn right, then go strait,
    # [-90, 100]
]

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def length(self):
        return math.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

    def ptOnLine(self, x, y):
        if (x >= self.x1 and x <= self.x2) or (x >= self.x2 and x <= self.x1):
            if (y >= self.y1 and y <= self.y2) or (y >= self.y2 and y <= self.y1):
                return True
        return False


class CoverageAlgorithm:
    def __init__(self, parkinglot, robot_width):
        self.parkinglot = parkinglot
        self.instructions = []
        self.robot_width = robot_width
        self.boundaries = []
        self.lines = []
        self.startDirection = 0.0
        self.axis = 0
        self.xMin = None
        self.xMax = None
        self.yMin = None
        self.yMax = None

    def getInstructions(self):
        # return MOCK_INSTRUCTIONS
        self.parsePoints(self.parkinglot)
        self.createInstructions()
        return self.instructions

    def parsePoints(self, parkingLot):
        for i in range(len(parkingLot) - 1):
            self.lines.append(Line(
                    parkingLot[i][0], 
                    parkingLot[i][1], 
                    parkingLot[i+1][0],
                    parkingLot[i+1][1]
            ))
            if self.xMin == None or parkingLot[i][0] < self.xMin:
                self.xMin = parkinglot[i][0]
            if self.yMin == None or parkingLot[i][1] < self.yMin:
                self.yMin = parkinglot[i][1]
            if self.xMax == None or parkingLot[i][0] > self.xMax:
                self.xMax = parkinglot[i][0]
            if self.yMax == None or parkingLot[i][1] > self.yMax:
                self.yMax = parkinglot[i][1]
            
        # self.lines.append(Line(self.parkingLot[len(self.parkingLot)-1][0], self.parkingLot[len(
        #     self.parkingLot)-1][1], self.parkingLot[0][0], self.parkingLot[0][1]))
        xBound = self.sliceLot(self.parkingLot)
        yBound = self.sliceLot(self.parkingLot, axis=1)
        # TODO: Find direction
        if len(xBound) < len(yBound):
            self.boundaries = xBound
            self.startDirection = 90
            self.axis = 0
        else:
            self.boundaries = yBound
            self.startDirection = 0
            self.axis = 1
        self.boundaries.sort()
        # m = max(yVals)
        # if m > yMax:
        #     yMax = m


    def sliceLot(self, points, axis=0):
        boundaries = []
        for point in points:
            if point[axis] not in boundaries:
                boundaries.append(point[axis])
            # if point[1] not in yVals:
            #     yVals.append(point[1])
        return boundaries

    def findMin(self, val):
        if self.axis == 0:
            for y in range(self.yMax + 1):
                for line in self.lines:
                    if line.ptOnLine(val, y):
                        return y
        elif self.axis == 1:
            for x in range(self.xMax + 1):
                for line in self.lines:
                    if line.ptOnLine(x, val):
                        return x
        return None

    def findMax(self, val):
        m = None
        if self.axis == 0:
            for y in range(self.xMax + 1):
                for line in self.lines:
                    if line.ptOnLine(val, y):
                        m = y
        elif self.axis == 1:
            for x in range(self.yMax + 1):
                for line in self.lines:
                    if line.ptOnLine(x, val):
                        m = x
        return m

    # def findMinYOnX(self, x):
    #     for y in range(yMax + 1):
    #         for line in lines:
    #             if line.ptOnLine(x, y):
    #                 return y
    #     return None


    # def findMaxYOnX(self, x):
    #     m = None
    #     for y in range(yMax + 1):
    #         for line in lines:
    #             if line.ptOnLine(x, y):
    #                 m = y
    #     return m


    def createInstructions(self):
        # TODO: move in direction found above rather than default
        # turn = self.startDirection
        for i in range(len(self.boundaries) - 1):
            # if self.axis == 0:
            distance = findMax(self.boundaries[i]) - findmin(self.boundaries[i])

            # elif self.axis == 1:
            #     distance = findMax(self.boundaries[i]) - findMin(self.boundaries[i])

            # boundStart = self.boundaries[i]
            # boundEnd = self.boundaries[i + 1]
            # Start = self.findMin(i)
            # End = self.findMax(i)

            # diffX = xEnd - xStart
            # print(f"goto({xStart},{yStart})")
            turn = self.startDirection
            self.instructions.append((turn,distance))
            for _ in range(0,distance,self.robot_width):
                # print(f"goforward({diffX})")
                # print(f"turn({turn})")
                # print(f"currentposition({xEnd}, {yStart})")
                self.instructions.append()
                # print(f"goforward({ROBOTLENGTH})")
                # print(f"turn({turn})")
                yStart += ROBOTLENGTH
                turn += 180
                turn %= 360
                # print(f"currentposition({xStart}, {yStart})")
                self.instructions.append([turn, (xEnd, yStart)])


    def reset(self):
        lines.clear()
        # verticalBoundaries.clear()
        yVals.clear()
        yMax = 0
        instructions.clear()



###################################################################################
import math





lines = []
verticalBoundaries = []
yVals = []
yMax = 0
instructions = []
horizBoundaries = []





lot1 = [
    (0, 50),
    (100, 50),
    (100, 0),
    (150, 0),
    (150, 100),
    (75, 100),
    (75, 75),
    (50, 75),
    (50, 100),
    (0, 100)
]

lot2 = [
    (0, 0),
    (100, 0),
    (100, 100),
    (0, 100),
]

print("parsing lot 1...")
parsePoints(lot1)
print(verticalBoundaries)
for x in verticalBoundaries:
    print(
        f"min-{x}: {findMinYOnX(x+ROBOTLENGTH)} -- max-{x}: {findMaxYOnX(x+ROBOTLENGTH)}")

createInstructions()
print(instructions)

RESET()

# print("parsing lot 2...")
# parsePoints(lot2)
# print(verticalBoundaries)
# for x in verticalBoundaries:
#     print(f"min-{x}: {findMinYOnX(x+ROBOTLENGTH)} -- max-{x}: {findMaxYOnX(x+ROBOTLENGTH)}")


'''
[0,25,50,100]
_________________________________________________
|        *                  *                     |
|        *                  *                     |
|        *                  *                     |
|        *                  *                     |
|        *                  *                     |
|        *                  *                     |
|________*                  * _____________________
        |                   |
        |                   |
        |___________________|                       

'''
# def invertParkinglot(parkinglot):
#     newParking = []
#     for i in range(len(parkinglot)):
#         parkinglot[i]