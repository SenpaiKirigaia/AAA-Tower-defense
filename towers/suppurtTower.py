from tower import Tower
import math


class RangeTower(Tower):
    """
    Add extra range to each surrounding tower
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 75
        self.effect = [0.2, 0.4]
        self.width = self.height = 90
        self.name = "range"
        self.price = [2000]

    def support(self, towers):
        """
        will modify towers according to ability
        """
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.range = tower.original_range + round(tower.range * self.effect[self.level - 1])


class DamageTower(RangeTower):
    """
    add damage to surrounding towers
    """

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 100
        self.effect = [0.5, 1]
        self.name = "damage"
        self.price = [2000]

    def support(self, towers):
        """
        will modify towers according to ability
        """
        effected = []
        for tower in towers:
            x = tower.x
            y = tower.y

            dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

            if dis <= self.range + tower.width / 2:
                effected.append(tower)

        for tower in effected:
            tower.damage = tower.original_damage + round(tower.original_damage * self.effect[self.level - 1])
