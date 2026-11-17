class Player:
    def __init__(self, name: str, max_strength: int, max_water: int, max_food: int, brain: Brain, vision_scope: Vision):
        self.name = name
        self.__inventory = []
        self.health = 100
        self.hunger = 0
        self.thirst = 0

        # using double underscore naming convention to show the variable is private
        self.__curr_strength = max_strength
        self.__curr_water = max_water
        self.__curr_food = max_food
        self.__curr_gold = 0

        self.__move_pts = 0
        self.__brain = brain
        self.__vision_scope = vision_scope

        self.curr_x = 0
        self.curr_y = 0