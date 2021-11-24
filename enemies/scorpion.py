from enemy import Enemy


class Scorpion(Enemy):
    def __init__(self):
        super().__init__()
        self.name = "scorpion"
        self.money = 1
        self.max_health = 1
        self.health = self.max_health
