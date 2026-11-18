import path
import map
import player
import terrain
import item

class Vision:
    neighboringSquares: tuple[int, int, int]                # number of squares visible to the [north, south, east]
    visionPath: path.Path                                   # a certain path from visible vision per brain's request (closestFood, closestWater, etc.)
    playerPos: tuple[int, int]                              # current position of player (x, y)
    visionMap: map.GameMap                                  # map stored for vision
    vision: list[list[terrain.Terrain]]                     # 2D array representation of current vision w/ visible terrain
    hasItems: list[tuple[tuple[int, int], int]]             # [hasItem square's x,y coords, distance]

    def __init__(self, neighboringSquares: tuple[int, int, int], map: map.GameMap, player: player.Player):
        self.neighboringSquares = neighboringSquares        # [north, south, east]
        self.playerPos = (player.currX, player.currY)
        self.visionMap = map
        self.vision = []
        self.hasItems = []
        self.visionPath = path.Path(0, 0, 0, 0)
        
        self.updateVision(self.playerPos[0], self.playerPos[1])
                
        
    def updateVision(self, currX: int, currY: int) -> list[list[terrain.Terrain]]:
        rangeNorth, rangeSouth, rangeEast = self.neighboringSquares
        
        for row in self.visionMap[currX - rangeNorth : currX + rangeSouth + 1]:
            selectCols = list(row[currY : currY + rangeEast + 1])
            self.vision.append(selectCols)
        
        return self.vision
        
    def closestFood(self) -> path.Path:
        hasFood = []
        for rowIndex, row in enumerate(self.vision):
            for colIndex, terrain in enumerate(row):
                terrainItem = terrain.getItem()
                
                if isinstance(terrainItem, item.Food):
                    foodDistance = abs(self.playerPos[0] - rowIndex) + abs(self.playerPos[1] - colIndex)
                    hasFood.append(((rowIndex, colIndex), foodDistance))
        
        self.hasItems = hasFood
        
        if not hasFood:
            print("No food seen in the vicinity.")
            return self.visionPath
        
        closestFood = min(hasFood, key=lambda x: x[1])
        
        foodX, foodY = closestFood[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            # max prevents movement direction from going negative
            max(playerX - foodX, 0),            # move north (player position - row index of closestFood)
            max(foodX - playerX, 0),            # move south (row index of closestFood - player position)
            max(foodY - playerY, 0),            # move east (col index of closestFood - player position)
            max(playerY - foodY, 0)             # move west (player positon - col index of closestFood)
        )
              
        return self.visionPath
    
    def secondClosestFood(self) -> path.Path:
        self.closestFood()                              # updates hasItems
        
        hasFood = self.hasItems.copy()
        
        if len(hasFood) < 2:
            print("Food is only seen once (or not seen) in the vicinity")
            return self.visionPath
        
        closest = min(hasFood, key=lambda x: x[1])
        hasFood.remove(closest)
        secondClosest = min(hasFood, key=lambda x: x[1])
        
        foodX, foodY = secondClosest[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            max(playerX - foodX, 0),
            max(foodX - playerX, 0),   
            max(foodY - playerY, 0),    
            max(playerY - foodY, 0)
        )
        
        return self.visionPath
        
    def closestWater(self) -> path.Path:
        hasWater = []
        
        for rowIndex, row in enumerate(self.vision):
            for colIndex, terrain in enumerate(row):
                terrainItem = terrain.getItem()
                
                if isinstance(terrainItem, item.Water):
                    waterDistance = abs(self.playerPos[0] - rowIndex) + abs(self.playerPos[1] - colIndex)
                    hasWater.append(((rowIndex, colIndex), waterDistance))
        
        self.hasItems = hasWater
        
        if not hasWater:
            print("No water seen in the vicinity.")
            return self.visionPath
        
        closestWater = min(hasWater, key=lambda x: x[1])
        
        waterX, waterY = closestWater[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            # max prevents movement direction from going negative
            max(playerX - waterX, 0),            # move north (player position - row index of closestWater)
            max(waterX - playerX, 0),            # move south (row index of closestWater - player position)
            max(waterY - playerY, 0),            # move east (col index of closestWater - player position)
            max(playerY - waterY, 0)             # move west (player positon - col index of closestWater)
        )
                
        return self.visionPath
    
    def secondClosestWater(self) -> path.Path:
        self.closestWater()                              # updates hasItems
        
        hasWater = self.hasItems.copy()
        
        if len(hasWater) < 2:
            print("Water is only seen once (or not seen) in the vicinity")
            return self.visionPath
        
        closest = min(hasWater, key=lambda x: x[1])
        hasWater.remove(closest)
        secondClosest = min(hasWater, key=lambda x: x[1])
        
        waterX, waterY = secondClosest[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            max(playerX - waterX, 0),
            max(waterX - playerX, 0),   
            max(waterY - playerY, 0),    
            max(playerY - waterY, 0)
        )
        return self.visionPath
    
    def closestGold(self) -> path.Path:
        hasGold = []
        
        for rowIndex, row in enumerate(self.vision):
            for colIndex, terrain in enumerate(row):
                terrainItem = terrain.getItem()
                
                if isinstance(terrainItem, item.Gold):
                    goldDistance = abs(self.playerPos[0] - rowIndex) + abs(self.playerPos[1] - colIndex)
                    hasGold.append(((rowIndex, colIndex), goldDistance))
        
        self.hasItems = hasGold
        
        if not hasGold:
            print("No gold seen in the vicinity.")
            return self.visionPath
        
        closestGold = min(hasGold, key=lambda x: x[1])
        
        goldX, goldY = closestGold[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            # max prevents movement direction from going negative
            max(playerX - goldX, 0),            # move north (player position - row index of closestGold)
            max(goldX - playerX, 0),            # move south (row index of closestGold - player position)
            max(goldY - playerY, 0),            # move east (col index of closestGold - player position)
            max(playerY - goldY, 0)             # move west (player positon - col index of closestGold)
        )
                
        return self.visionPath
    
    def secondClosestGold(self) -> path.Path:
        self.closestGold()                              # updates hasItems
        
        hasGold = self.hasItems.copy()
        
        if len(hasGold) < 2:
            print("Gold is only seen once (or not seen) in the vicinity")
            return self.visionPath
        
        closest = min(hasGold, key=lambda x: x[1])
        hasGold.remove(closest)
        secondClosest = min(hasGold, key=lambda x: x[1])
        
        goldX, goldY = secondClosest[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            max(playerX - goldX, 0),
            max(goldX - playerX, 0),   
            max(goldY - playerY, 0),    
            max(playerY - goldY, 0)
        )
        return self.visionPath
        
    def closestTrader(self) -> path.Path:
        hasTrader = []
        
        for rowIndex, row in enumerate(self.vision):
            for colIndex, terrain in enumerate(row):
                terrainItem = terrain.getItem()
                
                if isinstance(terrainItem, item.Trader):
                    traderDistance = abs(self.playerPos[0] - rowIndex) + abs(self.playerPos[1] - colIndex)
                    hasTrader.append(((rowIndex, colIndex), traderDistance))
        
        self.hasItems = hasTrader
        
        if not hasTrader:
            print("No trader seen in the vicinity.")
            return self.visionPath
        
        closestTrader = min(hasTrader, key=lambda x: x[1])
        
        traderX, traderY = closestTrader[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            # max prevents movement direction from going negative
            max(playerX - traderX, 0),            # move north (player position - row index of closestTrader)
            max(traderX - playerX, 0),            # move south (row index of closestTrader - player position)
            max(traderY - playerY, 0),            # move east (col index of closestTrader - player position)
            max(playerY - traderY, 0)             # move west (player positon - col index of closestTrader)
        )
                
        return self.visionPath
    
    def secondClosestTrader(self) -> path.Path:
        self.closestTrader()                              # updates hasItems
        
        hasTrader = self.hasItems.copy()
        
        if len(hasTrader) < 2:
            print("Trader is only seen once (or not seen) in the vicinity")
            return self.visionPath
        
        closest = min(hasTrader, key=lambda x: x[1])
        hasTrader.remove(closest)
        secondClosest = min(hasTrader, key=lambda x: x[1])
        
        traderX, traderY = secondClosest[0]
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
            max(playerX - traderX, 0),
            max(traderX - playerX, 0),   
            max(traderY - playerY, 0),    
            max(playerY - traderY, 0)
        )
        return self.visionPath
    
    def easiestPath(self) -> path.Path:
        leastMoveCost = 10000                   # arbitary initial number to get least cost
        leastCostSquare = ()
        
        for rowIndex, row in enumerate(self.vision):
                for colIndex, terrain in enumerate(row):
                    terrainMoveCost = terrain.movementCost
                    if terrainMoveCost < leastMoveCost:
                        leastCostSquare = (rowIndex, colIndex)
        
        leastX, leastY = leastCostSquare
        playerX, playerY = self.playerPos
        
        self.visionPath = path.Path(
                    max(playerX - leastX, 0),
                    max(leastX - playerX, 0),   
                    max(leastY - playerY, 0),    
                    max(playerY - leastY, 0)
                )
        return self.visionPath
    
    
    