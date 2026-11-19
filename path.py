class Path:
    moveNorth = 0
    moveSouth = 0
    moveEast = 0
    moveWest = 0
    diagonalMoves = []
    
    movementPath = []
    
    totalMoveCost = 0
    totalWaterCost = 0
    totalFoodCost = 0
    
    def __init__(self, north, south, east, west):
        self.moveNorth = north
        self.moveSouth = south
        self.moveEast = east
        self.moveWest = west
        
        self.movementPath = self.movementPath.extend([north, south, east, west])
        self.totalMoveCost = north + south + east + west
    
    def getMovementCost(self) -> int:
        return self.totalMoveCost
    
    def getWaterCost(self) -> int:
        return self.totalWaterCost
    
    def getFoodCost(self) -> int:
        return self.totalFoodCost