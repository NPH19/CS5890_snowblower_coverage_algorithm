

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
    # turn right and reposition for the next swath
    [-90, 10],
    # turn right, then go strait,
    [-90, 100]
]


class CoverageAlgorithm:
    def __init__(self, parkinglot):
        self.parkinglot = parkinglot
        self.instructions = []

    def getInstructions(self):
        return MOCK_INSTRUCTIONS
