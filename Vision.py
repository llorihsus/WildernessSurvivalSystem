import Path

class Vision:
    neighboringSquares = []
    path = Path(0, 0, 0, 0)
    
    def __init__(self, neighboringSquares):
        self.neighboringSquares = neighboringSquares
        
    def updateVision(self, map, currX, currY):
        return
        
    def closestFood(self) -> Path:
        return self.path
    
    def secondClosestFood(self) -> Path:
        return self.path
        
    def closestWater(self) -> Path:
        return self.path
    
    def secondClosestWater(self) -> Path:
        return self.path
    
    def closestGold(self) -> Path:
        return self.path
    
    def secondClosestGold(self) -> Path:
        return self.path
        
    def closestTrader(self) -> Path:
        return self.path
    
    def secondClosestTrader(self) -> Path:
        return self.path
    
    def easiestPath(self) -> Path:
        return self.path
    
    
    