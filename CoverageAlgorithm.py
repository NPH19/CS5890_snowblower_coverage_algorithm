

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
                self.xMin = parkingLot[i][0]
            if self.yMin == None or parkingLot[i][1] < self.yMin:
                self.yMin = parkingLot[i][1]
            if self.xMax == None or parkingLot[i][0] > self.xMax:
                self.xMax = parkingLot[i][0]
            if self.yMax == None or parkingLot[i][1] > self.yMax:
                self.yMax = parkingLot[i][1]
        
        print(self.xMax, self.xMin, self.yMax, self.yMin)

        xBound = self.sliceLot(parkingLot)
        yBound = self.sliceLot(parkingLot, axis=1)
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
        print(self.boundaries)

    def sliceLot(self, points, axis=0):
        boundaries = []
        for point in points:
            if point[axis] not in boundaries:
                boundaries.append(point[axis])
        return boundaries

    def findMin(self, val):
        if self.axis == 0:
            for y in range(self.yMin, self.yMax + 1):
                for line in self.lines:
                    if line.ptOnLine(val, y):
                        print("min y: " + str(y))
                        return y
        elif self.axis == 1:
            for x in range(self.xMin, self.xMax + 1):
                for line in self.lines:
                    if line.ptOnLine(x, val):
                        print("min x: " + str(x))
                        return x
        return None

    def findMax(self, val):
        m = None
        if self.axis == 0:
            for y in range(self.yMin, self.yMax + 1):
                for line in self.lines:
                    if line.ptOnLine(val, y):
                        m = y
        elif self.axis == 1:
            for x in range(self.xMin, self.xMax + 1):
                for line in self.lines:
                    if line.ptOnLine(x, val):
                        m = x
        print("max: " + str(m))
        return m

    def createInstructions(self):
        # TODO: move in direction found above rather than default
        for i in range(len(self.boundaries) - 1):
            distance = self.findMax(self.boundaries[i]) - self.findMin(self.boundaries[i])
            range_ = self.boundaries[i + 1] - self.boundaries[i]
            turn = self.startDirection + 90
            for _ in range(0,range_,self.robot_width):
                self.instructions.append((turn,distance))
                self.instructions.append((turn,self.robot_width))
                self.instructions.append((turn,distance))
                turn += 180
                turn %= 360
                self.instructions.append((turn,self.robot_width))

###################################################################################
# import math

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

algo = CoverageAlgorithm(lot1, 10)
instructions = algo.getInstructions()
print(instructions)

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