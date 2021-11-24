from tower import Tower
import math


class ArcherTowerLong(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.archer_count = 0
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 1
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "archer"

    def change_range(self, r):
        """
        change range of archer tower
        """
        self.range = r

    def attack(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        """
        money = 0
        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            x = enemy.x
            y = enemy.y

            dis = math.sqrt(
                (self.x - enemy.img.get_width() / 2 - x) ** 2 + (self.y - enemy.img.get_height() / 2 - y) ** 2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == 50:
                if first_enemy.hit(self.damage):
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)

            if first_enemy.x > self.x and not self.left:
                self.left = True
            elif self.left and first_enemy.x < self.x:
                self.left = False

        return money


class ArcherTowerShort(ArcherTowerLong):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.archer_count = 0
        self.range = 120
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 2
        self.original_damage = self.damage
        self.name = "archer2"
