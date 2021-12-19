import copy
import utils.base_utils as base_utils


class BattleField:
    '''
    Class of the game environment
    '''
    '''
    Класс игрового окружения
    '''

    base_hp = base_utils.Bar()

    def __init__(self, max_base_hp, tower_space, waves, enemy_path):
        '''
        Init method of the game environment
        :param max_base_hp: max health points of the base
        :param tower_space: list with places available to place towers
        :param waves: list with enemy waves
        :param enemy_path: list with enemy path
        '''
        '''
        Метод инициализации игрового окружения
        :param max_base_hp: максимальное кол-во здоровья базы
        :param tower_space: список с местами доступными для застройки башнями
        :param waves: список с волнами врагов
        :param enemy_path: список с путем врагов
        '''

        self.base_hp = (0, max_base_hp, max_base_hp)
        self.money = 2000

        self.tower_space = tower_space
        self.enemy_path = enemy_path

        self.enemies = []
        self.towers = []
        self.enemy_generator = EnemyGenerator(waves, enemy_path, self)

        self.fresh_objs = []
        self.del_objs = []

    def get_enemies(self):
        '''
        Method that returns the list with all enemies
        '''
        '''
        Метод, возвращающий списко со всеми врагами
        '''

        return self.enemies

    def get_towers(self):
        '''
        Method that returns the list with all towers
        '''
        '''
        Метод, возвращающий списко со всеми башнями
        '''

        return self.towers

    def get_wave_data(self):
        '''
        Method that wraps the enemy generator get_wave_data
        '''
        '''
        Метод-обертка для  метода get_wave_data генератора врагов
        '''

        return self.enemy_generator.get_wave_data()

    def income(self, money):
        '''
        Method that receive income
        '''
        '''
        Метод, примающий доход
        '''

        self.money += money

    def hit_base(self, dmg):
        '''
        Method that registers damage to the base
        :param dmg: dealt damage
        '''
        '''
        Метод, регистрирующий урон по базе
        :param dmg: нанесенный урон
        '''

        self.base_hp -= dmg

    def can_buy(self, tower_type):
        '''
        Method that checks the ability to but the tower
        of given type
        :param tower_type: type of tower to check for
        '''
        '''
        Метод, проверяющий возможность покупки данного типа
        башен
        :param tower_type: тип башен, для которого нужно проверить
                           возможность покупки
        '''

        return tower_type.price <= self.money

    def get_free_space(self, tower_type):
        '''
        Method that returns available space to place tower of the
        given type
        :param tower_type: type of the tower to check for
        '''
        '''
        Метод, возвращающий возможные места для застройки данным типом
        башен
        :param tower_type: тип башен, для которого нужно проверить
                           возможность застройки
        '''

        if tower_type.price <= self.money:
            return copy.deepcopy(self.tower_space)
        else:
            return list()

    def buy_tower(self, tower_pos, tower_type):
        '''
        Method that buys the tower of the given type and place
        it on given coords
        :param tower_pos: position to place tower on
        :param tower_type: type of the bought tower
        '''
        '''
        Метод, покупающий башню данного типа и устанавливающий
        ее на данную позицию
        :param tower_pos: позиция для установки башни
        :param tower_type: тип, купленной башни
        '''

        if tower_type.price <= self.money:
            new_tower = tower_type.get_tower(self, tower_pos)

            self.towers.append(new_tower)
            self.fresh_objs.append(new_tower)

            self.tower_space.remove(tower_pos)
            self.money -= tower_type.price
            return True
        else:
            return False

    def get_occupied_space(self):
        '''
        Method that returns list of place occupied by towers
        '''
        '''
        Метод, возращающий список с местми, занятыми башнями
        '''

        occupied_space = [tower.pos for tower in self.towers]
        return copy.deepcopy(occupied_space)

    def sell_tower(self, tower_pos):
        '''
        Method that sells the tower on the given position
        :tower_pos: position of tower to sell
        '''
        '''
        Метод, продающий башню на данной позиции
        :tower_pos: позиция башни, которую нужно продать
        '''

        for tower in self.towers:
            if tower.pos == tower_pos:
                self.towers.remove(tower)
                self.del_objs.append(tower)
                self.money += tower.sell()
                self.tower_space.append(tower_pos)

    def check_end(self):
        '''
        Method that checks for gameover
        '''
        '''
        Метод, проверяющий закончалась ли игра
        '''

        wave_flag = len(self.enemy_generator.waves) == 0
        enemy_flag = len(self.enemies) == 0
        health_flag = self.base_hp == 0

        return (wave_flag and enemy_flag) or health_flag

    def update(self, dt):
        '''
        Method that updates the game environment
        :param dt: amount of passed time
        '''
        '''
        Метод, обновляющий игровое окружение
        :param dt: кол-во прошедшего времени
        '''

        for enemy in self.enemies:
            enemy.run(dt)

        for tower in self.towers:
            tower.run(dt)

        dead_enemies = []
        for enemy in self.enemies:
            if not enemy.is_alive():
                dead_enemies.append(enemy)

        for enemy in dead_enemies:
            self.del_objs.append(enemy)
            self.enemies.remove(enemy)

        self.enemy_generator.run(dt)
        self.enemy_generator.generate_enemy()
        return not self.check_end()


class EnemyGenerator:
    '''
    Class of enemy generator
    '''
    '''
    Класс генератора врагов
    '''

    def __init__(self, waves, enemy_path, battle_field):
        '''
        Init method of enemy generator
        :param waves: list with enemy waves
        :param enemy_path: list with enemy path
        :param battle_fied: link to the current game environment
        '''
        '''
        Метод инициализации генератора врагов
        :param waves: список с волнами врагов
        :param enemy_path: список с путем врагов
        :param battle_field: ссылка на текущее игровое окружение
         '''

        self.waves = waves
        self.enemy_path = enemy_path
        self.battle_field = battle_field

        self.total_waves_number = len(self.waves)
        self.enemy_timer = base_utils.Timer(5)
        self.wave_timer = base_utils.Timer(10)

    def generate_enemy(self):
        '''
        Method that generates new enemy
        '''
        '''
        Метод, создающий нового врага
        '''

        if self.wave_timer.is_ringing():
            if self.enemy_timer.is_ringing():
                if len(self.waves) > 0:
                    enemy_factory = self.waves[0].pop(0)
                    new_enemy = enemy_factory.get_enemy(self.battle_field,
                                                        self.enemy_path)
                    self.battle_field.enemies.append(new_enemy)
                    self.battle_field.fresh_objs.append(new_enemy)
                    self.enemy_timer.reset()
                    if len(self.waves[0]) == 0:
                        self.waves.pop(0)
                        self.wave_timer.reset()

    def run(self, dt):
        '''
        Method that describes enemy generator default behaviour
        :param dt: amount of passed time
        '''
        '''
        Метод, описывающий дефолтное поведение генератора врагов
        :param dt: кол-во прошедшего времени
        '''

        if self.wave_timer.is_ringing():
            self.enemy_timer.update(dt)
        else:
            self.wave_timer.update(dt)

        return len(self.waves) > 0

    def get_wave_data(self):
        '''
        Method that returns the wave data
        (current wave number, total waves number)
        '''
        '''
        Метод, возвращающий кортеж с номером, текущий волны,
        общим кол-вом волн
        '''

        curr_wave_number = self.total_waves_number - len(self.waves) + 1
        curr_wave_number = min(curr_wave_number, self.total_waves_number)
        return (curr_wave_number, self.total_waves_number)
