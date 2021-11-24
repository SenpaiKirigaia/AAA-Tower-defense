import pygame


class Tower:
    """
    Class for towers
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 1
        self.selected = False
        self.damage = 1
        self.tower_imgs = []
        self.place_color = (0, 0, 255, 100)

    def draw_radius(self, win):
        if self.selected:
            # draw range circle
            surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):
        # draw range circle
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, self.place_color, (50, 50), 50, 0)

        win.blit(surface, (self.x - 50, self.y - 50))

    def sell(self):
        """
        call to sell the tower, returns sell price
        """
        return self.sell_price[self.level - 1]

    def upgrade(self):
        """
        upgrades the tower for a given cost
        """
        if self.level < len(self.tower_imgs):
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        """
        returns the upgrade cost, if 0 then can't upgrade anymore
        """
        return self.price[self.level - 1]
