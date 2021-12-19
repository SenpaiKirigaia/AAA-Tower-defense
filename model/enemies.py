import copy
import random
import utils.base_utils as base_utils
import utils.state_utils as state_utils


class Enemy:
    '''
    Basic class of the enemy
    '''
    '''
    Базовый класс врага
    '''

    hp = base_utils.Bar()

    def __init__(self, type_name, state_lib, max_hp, vel,
                 reward, battle_field, path):
        '''
        Init method of enemy
        :param type_name: type of the enemy
        :param state_lib: object of StateLib class with possible states
                          of the enemy
        :param max_hp: max health points of the enemy
        :param vel: velocity of the enemy
        :param reward: reward for killing the enemy
        :param battle_field: link to the current game environment
        :param path: path of the enemy
        '''
        '''
        Метод инициализации врага
        :param type_name: тип врага
        :param state_lib: объект класса StateLib со всеми возможными
                          состояниями врага
        :param max_hp: максимальное кол-во здоровья врага
        :param vel: скорость движения врага
        :param reward: награда за убийство врага
        :param battle_field: ссылка на текущее игровое окружение
        :param path: путь движения врага
        '''

        self.type_name = type_name
        self.state_lib = state_lib

        self.hp = (0, max_hp, max_hp)
        self.vel = vel
        self.reward = reward

        self.path = base_utils.SafeIter(path)
        self.battle_field = battle_field
        self.pos = list(self.path.current())

        self.direct = base_utils.DIR.E
        self.state = self.state_lib.default()

    def run(self, dt):
        '''
        Method that describes default behaviour of the enemy
        :param dt: amount of passed time
        '''
        '''
        Метод, описывающий дефолтное поведение врагов
        :param dt: кол-во прошедшего времени
        '''

        if self.state.name != self.state_lib.names.dying:
            if self.state.name != self.state_lib.names.default:
                if self.state.is_ringing():
                    self.state = self.state_lib.default()

            self.move(dt)
        self.state.update(dt)

    def move(self, dt):
        '''
        Method that describes movement of the enemy
        :param dt: amount of passed time
        '''
        '''
        Метод, описывающий движение врагов
        :param dt: кол-во прошедшего времени
        '''

        goal = self.path.current()
        diff_pos = (self.pos[0] - goal[0])**2 + (self.pos[1] - goal[1])**2
        if diff_pos < 10**2:
            if self.path.at_end():
                self.battle_field.hit_base(1)
                self.state = self.state_lib.dying()
            else:
                self.path.next()

        vec_x = self.path.current()[0] - self.pos[0]
        vec_y = self.path.current()[1] - self.pos[1]

        norm_x, norm_y = base_utils.vec_norm(vec_x, vec_y)
        if norm_x >= 0:
            self.direct = base_utils.DIR.E
        else:
            self.direct = base_utils.DIR.W

        if norm_y >= 0:
            self.direct |= base_utils.DIR.S
        else:
            self.direct |= base_utils.DIR.N

        self.pos[0] += norm_x * self.vel * dt
        self.pos[1] += norm_y * self.vel * dt

    def is_alive(self):
        '''
        Method that checks if the enemy is alive
        '''
        '''
        Метод, проверяющий жив ли враг
        '''

        if (self.state.name == self.state_lib.names.dying
           and self.state.is_ringing()):
            return False
        else:
            return True

    def hit(self, dmg):
        '''
        Method that registers damage to the enemy
        :param dmg: dealt damage
        '''
        '''
        Метод, регистрирующий урон по базе
        :param dmg: нанесенный урон
        '''

        self.state = self.state_lib.hurt()
        self.hp -= dmg
        if self.hp == 0:
            self.battle_field.income(self.reward)
            self.state = self.state_lib.dying()


class EnemyFactory:
    '''
    Class of enemy factory
    '''
    '''
    Класс фабрики, создающей врагов
    '''

    def __init__(self, type_name, states, max_hp, vel, reward):
        '''
        Init method of enemy factory
        :param type_name: type of the enemy
        :param states: dict with all possible states of the enemy
        :param max_hp: max health points of the enemy
        :param vel: velocity of the enemy
        :param reward: reward for killing the enemy
        '''
        '''
        Метод инициализации фабрики, создающей врагов
        :param type_name: тип врага
        :param states: словарь со всеми возможными состояниями врага
        :param max_hp: максимальное кол-во здоровья врага
        :param vel: скорость движения врага
        :param reward: награда за убийство врага
        '''

        self.type_name = type_name
        self.state_lib = state_utils.StateLib(states)
        self.max_hp = max_hp
        self.vel = vel
        self.reward = reward

    def get_enemy(self, battle_field, path):
        '''
        Method that generates new enemy
        :param battle_field: link to the current game environment
        :param path: path of the enemy
        '''
        '''
        Метод, создающий нового врага
        :param battle_field: ссылка на текущее игровое окружение
        :param path: путь движения врага
         '''
        new_path = copy.deepcopy(path)
        for point in new_path:
            point[0] += random.randint(-20, 20)
            point[1] += random.randint(-20, 20)
        return Enemy(self.type_name, self.state_lib, self.max_hp, self.vel,
                     self.reward, battle_field, new_path)


ENEMY_TYPES = {
               "SCORPION": EnemyFactory("SCORPION",
                                        states={
                                                "default": 1,
                                                "hurt": 4,
                                                "dying": 4
                                               },
                                        max_hp=100, vel=80, reward=100),
               "SPHINX": EnemyFactory("SPHINX",
                                      states={
                                              "default": 1,
                                              "hurt": 2,
                                              "dying": 2
                                             },
                                      max_hp=50, vel=130, reward=90),
               "SNAKE": EnemyFactory("SNAKE",
                                     states={
                                             "default": 1,
                                             "hurt": 6,
                                             "dying": 6
                                            },
                                     max_hp=250, vel=50, reward=150)
               }
