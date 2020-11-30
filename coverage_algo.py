import math

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
    
ROBOTLENGTH = 5
lines = []
verticalBoundaries = []
yVals = []
yMax = 0
instructions = []

def parsePoints(listOfPoints):
    global lines, verticalBoundaries, yMax, yVals
    for i in range(len(listOfPoints) - 1):
        lines.append(Line(listOfPoints[i][0], listOfPoints[i][1], listOfPoints[i+1][0], listOfPoints[i+1][1]))
    lines.append(Line(listOfPoints[len(listOfPoints)-1][0],listOfPoints[len(listOfPoints)-1][1],listOfPoints[0][0],listOfPoints[0][1]))

    for point in listOfPoints:
        if point[0] not in verticalBoundaries:
            verticalBoundaries.append(point[0])
        if point[1] not in yVals:
            yVals.append(point[1])

    verticalBoundaries.sort()
    m = max(yVals)
    if m > yMax:
        yMax = m

def findMinYOnX(x):
    global yMax
    for y in range(yMax + 1):
        for line in lines:
            if line.ptOnLine(x,y):
                return y
    return None

def findMaxYOnX(x):
    global yMax
    m = None
    for y in range(yMax + 1):
        for line in lines:
            if line.ptOnLine(x,y):
                m = y
    return m

def createInstructions():
    global lines, verticalBoundaries, yVals, yMax, instructions
    for i in range(len(verticalBoundaries) - 1):
        xStart = verticalBoundaries[i]
        xEnd = verticalBoundaries[i + 1]
        yStart = findMinYOnX(xStart)
        yEnd = findMaxYOnX(xStart)

        diffX = xEnd - xStart
        print(f"goto({xStart},{yStart})")
        instructions.append((xStart, yStart))
        turn = -90
        while yStart < yEnd:
            # print(f"goforward({diffX})")
            # print(f"turn({turn})")
            # print(f"currentposition({xEnd}, {yStart})")
            instructions.append((xEnd, yStart))
            # print(f"goforward({ROBOTLENGTH})")
            # print(f"turn({turn})")
            yStart += ROBOTLENGTH
            turn *= -1
            # print(f"currentposition({xStart}, {yStart})")
            instructions.append((xStart, yStart))
    

def RESET():
    global lines, verticalBoundaries, yVals, yMax, instructions
    lines.clear()
    verticalBoundaries.clear()
    yVals.clear()
    yMax = 0
    instructions.clear()


lot1 = [
    (0,50),
    (100,50),
    (100,0),
    (150,0),
    (150,100),
    (75,100),
    (75,75),
    (50,75),
    (50,100),
    (0,100)
]

lot2 = [
    (0,0),
    (100,0),
    (100,100),
    (0,100),
]

print("parsing lot 1...")
parsePoints(lot1)
print(verticalBoundaries)
for x in verticalBoundaries:
    print(f"min-{x}: {findMinYOnX(x+ROBOTLENGTH)} -- max-{x}: {findMaxYOnX(x+ROBOTLENGTH)}")

createInstructions()
print(instructions)

RESET()

# print("parsing lot 2...")
# parsePoints(lot2)
# print(verticalBoundaries)
# for x in verticalBoundaries:
#     print(f"min-{x}: {findMinYOnX(x+ROBOTLENGTH)} -- max-{x}: {findMaxYOnX(x+ROBOTLENGTH)}")