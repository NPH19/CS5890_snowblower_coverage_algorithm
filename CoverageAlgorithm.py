from math import sqrt

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
        return sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)

    def ptOnLine(self, x, y):
        if (x >= self.x1 and x <= self.x2) or (x >= self.x2 and x <= self.x1):
            if (y >= self.y1 and y <= self.y2) or (y >= self.y2 and y <= self.y1):
                return True
        return False


class CoverageAlgorithm:
    def __init__(self, parkinglot, robot_width, cellsize):
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
        self.cellsize = cellsize

    def getInstructions(self):
        # return MOCK_INSTRUCTIONS
        print('parking lot: ',self.parkinglot)
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
                self.xMin = self.parkinglot[i][0]
            if self.yMin == None or parkingLot[i][1] < self.yMin:
                self.yMin = self.parkinglot[i][1]
            if self.xMax == None or parkingLot[i][0] > self.xMax:
                self.xMax = self.parkinglot[i][0]
            if self.yMax == None or parkingLot[i][1] > self.yMax:
                self.yMax = self.parkinglot[i][1]

        xBound = self.sliceLot(self.parkinglot)
        yBound = self.sliceLot(self.parkinglot, axis=1)
        if len(xBound) < len(yBound):
            self.boundaries = xBound
            self.startDirection = 0
            self.axis = 0
            print('splitting horizontally')
        else:
            self.boundaries = yBound
            self.startDirection = 0
            self.axis = 1
            print('splitting vertically')
        self.boundaries.sort()

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
        for i in range(len(self.boundaries) - 1):
            distance = self.findMax(self.boundaries[i]) - self.findMin(self.boundaries[i])
            distance -= self.robot_width
            range_ = self.boundaries[i + 1] - self.boundaries[i] - self.robot_width
            turn = self.startDirection
            self.instructions.append((turn,int(distance/self.cellsize)))
            if self.axis == 0:
                sign = -1
            else:
                sign = 1

            for _ in range(0,range_-1,self.robot_width):
                sign *= -1
                side_step = self.robot_width
                turn = sign * 90
                self.instructions.append((turn,int(side_step/self.cellsize)))
                turn = sign * 90
                self.instructions.append((turn, int(distance/self.cellsize)))
            # TODO: get to next cell
            # Finding start position of next cell (top left?)
            # Goto command?
