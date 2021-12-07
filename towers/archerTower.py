import pygame
from .tower import Tower
import os
import math
from menu.menu import Menu


menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")).convert_alpha(), (120, 70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade.png")).convert_alpha(), (50, 50))


tower_imgs1 = []
archer_imgs1 = []
# load archer tower images
for x in range(1):
    tower_imgs1.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_1", str(x) + ".png")).convert_alpha(),
        (90, 90)))

# load archer images
for x in range(1):
    archer_imgs1.append(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top", str(x) + ".png")).convert_alpha())


class ArcherTowerLong(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs1[:]
        self.archer_imgs = archer_imgs1[:]
        self.archer_count = 0
        self.archer_fire_time = 240
        self.range = 200
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 2
        self.original_damage = self.damage
        self.width = self.height = 90
        self.moving = False
        self.name = "archer"
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, 5000,"MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the arhcer tower and animated archer
        """
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.archer_count += 1
        else:
            self.archer_count = 0

        archer = self.archer_imgs[0]
        if self.left == True:
            add = -25
        else:
            add = -archer.get_width() + 10
        win.blit(archer, ((self.x + add), (self.y - archer.get_height() - 25)))

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

            distance = math.sqrt((self.x - enemy.img.get_width()/2 - x)**2 + (self.y - enemy.img.get_height()/2 - y)**2)
            if distance <= self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            if self.archer_count == self.archer_fire_time:
                first_enemy.hit(self.damage)
                if first_enemy.alive:
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)
            """
            if first_enemy.x > self.x and not(self.left):
                self.left = True
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
                    
            elif self.left and first_enemy.x < self.x:
                self.left = False
                for x, img in enumerate(self.archer_imgs):
                    self.archer_imgs[x] = pygame.transform.flip(img, True, False)
            """
        return money


tower_imgs = []
archer_imgs = []
# load archer tower images
for x in range(1):
    tower_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_2", str(x) + ".png")),
        (90, 90)))

# load archer images
for x in range(1):
    archer_imgs.append(
        pygame.image.load(os.path.join("game_assets/archer_towers/archer_top_2", str(x) + ".png")))


class ArcherTowerShort(ArcherTowerLong):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.tower_imgs = tower_imgs[:]
        self.archer_imgs = archer_imgs[:]
        self.archer_count = 0
        self.archer_fire_time = 150
        self.range = 120
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 2
        self.original_damage = self.damage

        self.menu = Menu(self, self.x, self.y, menu_bg, [2500, 5500, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")
        self.name = "archer2"



