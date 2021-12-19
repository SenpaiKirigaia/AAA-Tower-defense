import utils.state_utils as state_utils


class Tower:
    '''
    Basic class of the tower
    '''
    '''
    Базовый класс башни
    '''

    def __init__(self, type_name, state_lib, act_range,
                 price, sell_price, battle_field, pos):
        '''
        Init method of tower
        :param type_name: type of the tower
        :param state_lib: object of StateLib class with possible states
                          of the tower
        :param act_range: active range of the tower
        :param price: price of the tower
        :param sell_price: sell price of the tower
        :param battle_field: link to the current game environment
        :param pos: (x, y) - position of the tower
        '''
        '''
        Метод инициализации башни
        :param type_name: тип башни
        :param state_lib: объект класса StateLib со всеми возможными
                          состояниями башни
        :param act_range: активный радиус башни
        :param price: цена покупки башни
        :param sell_price: деньги, получаемые за продажу башни
        :param battle_field: ссылка на текущее игровое окружение
        :param pos: (x, y) - позиция башни
        '''

        self.type_name = type_name
        self.pos = pos
        self.state_lib = state_lib
        self.state = self.state_lib.default()
        self.battle_field = battle_field

        self.act_range = act_range
        self.price = price
        self.sell_price = sell_price

    def sell(self):
        '''
        Method that returns sell price of the tower
        '''
        '''
        Метод, возвращающий цену продажи башни
        '''

        return self.sell_price

    def run(self, dt):
        '''
        Method that describes default behaviour of the tower
        :param dt: amount of passed time
        '''
        '''
        Метод, описывающий дефолтное поведение башни
        :param dt: кол-во прошедшего времени
        '''

        if self.state.is_ringing():
            if self.state != self.state_lib.names.default:
                self.state = self.state_lib.default()

        self.state.update(dt)


class TowerFactory:
    '''
    Class of tower factory
    '''
    '''
    Класс фабрики, создающей башни
    '''

    def __init__(self, type_name, states, act_range, price,
                 sell_price):
        '''
        Init method of tower factory
        :param type_name: type of the tower
        :param states: dict with all possible states
                       of the tower
        :param act_range: active range of the tower
        :param price: price of the tower
        :param sell_price: sell price of the tower
        '''
        '''
        Метод инициализации фабрики, создающей башни
        :param type_name: тип башни
        :param states: словарь со всеми возможными
                       состояниями башни
        :param act_range: активный радиус башни
        :param price: цена покупки башни
        :param sell_price: деньги, получаемые за продажу башни
        '''

        self.type_name = type_name
        self.state_lib = state_utils.StateLib(states)
        self.act_range = act_range
        self.price = price
        self.sell_price = sell_price

    def get_tower(self, pos, battle_field):
        '''
        Method that generates new tower
        :param battle_field: link to the current game environment
        :param pos: (x, y) - position of the tower
        '''
        '''
        Метод, создающий новую башню
        :param battle_field: ссылка на текущее игровое окружение
        :param pos: (x, y) - позиция башни
         '''
        return Tower(self.type_name, self.state_lib, pos, battle_field,
                     self.act_range, self.price,
                     self.sell_price)


class AttackTower(Tower):
    '''
    Class of the attack tower
    '''
    '''
    Класс атакующих башен
    '''

    def __init__(self, type_name, state_lib, act_range, dmg, price,
                 sell_price, battle_field, pos):
        '''
        Init method of attack tower
        :param type_name: type of the attack tower
        :param state_lib: object of StateLib class with possible states
                          of the tower
        :param act_range: active range of the tower
        :param dmg: damage dealt by the tower
        :param price: price of the tower
        :param sell_price: sell price of the tower
        :param battle_field: link to the current game environment
        :param pos: (x, y) - position of the tower
        '''
        '''
        Метод инициализации атакующей башни
        :param type_name: тип башни
        :param state_lib: объект класса StateLib со всеми возможными
                          состояниями башни
        :param act_range: активный радиус башни
        :param dmg: урон, наносимый башней
        :param price: цена покупки башни
        :param sell_price: деньги, получаемые за продажу башни
        :param battle_field: ссылка на текущее игровое окружение
        :param pos: (x, y) - позиция башни
        '''

        super().__init__(type_name, state_lib, act_range,
                         price, sell_price, battle_field, pos)
        self.dmg = dmg

    def attack(self, enemies):
        '''
        Method that describes attack behaviour of the tower
        :param enemies: possible targets for the tower
        '''
        '''
        Метод, описывающий атакующее поведение башни
        :param enemies: возможные цели для башни
        '''

        tower_pos = self.pos

        inrange_enemies = []
        for enemy in enemies:
            enemy_pos = enemy.pos
            sq_dist = ((tower_pos[0] - enemy_pos[0])**2
                       + (tower_pos[1] - enemy_pos[1])**2)
            if sq_dist <= self.act_range ** 2:
                inrange_enemies.append(enemy)

        if len(inrange_enemies) > 0:
            closest_enemy = max(inrange_enemies,
                                key=lambda enemy: enemy.path.indx)
            closest_enemy.hit(self.dmg)
            self.state = self.state_lib.attack()

    def run(self, dt):
        '''
        Method that describes default behaviour of the tower
        :param dt: amount of passed time
        '''
        '''
        Метод, описывающий дефолтное поведение башни
        :param dt: кол-во прошедшего времени
        '''

        super().run(dt)
        if self.state.is_ringing():
            if self.state.name == self.state_lib.names.default:
                self.attack(self.battle_field.get_enemies())

            elif self.state.name == self.state_lib.names.attack:
                self.state = self.state_lib.cool_down()


class AttackTowerFactory(TowerFactory):
    '''
    Class of attack tower factory
    '''
    '''
    Класс фабрики, создающей атакующие башни
    '''

    def __init__(self, type_name, states, act_range, dmg, price,
                 sell_price):
        '''
        Init method of attack tower factory
        :param type_name: type of the tower
        :param states: dict with all possible states
                       of the tower
        :param act_range: active range of the tower
        :param dmg: damage dealt by the tower
        :param price: price of the tower
        :param sell_price: sell price of the tower
        '''
        '''
        Метод инициализации фабрики, создающей башни
        :param type_name: тип башни
        :param states: словарь со всеми возможными
                       состояниями башни
        :param act_range: активный радиус башни
        :param dmg: урон, наносимый башней
        :param price: цена покупки башни
        :param sell_price: деньги, получаемые за продажу башни
        '''

        super().__init__(type_name, states, act_range, price, sell_price)
        self.dmg = dmg

    def get_tower(self, battle_field, pos):
        '''
        Method that generates new tower
        :param battle_field: link to the current game environment
        :param pos: (x, y) - position of the tower
        '''
        '''
        Метод, создающий новую башню
        :param battle_field: ссылка на текущее игровое окружение
        :param pos: (x, y) - позиция башни
        '''
        return AttackTower(self.type_name, self.state_lib, self.act_range,
                           self.dmg, self.price, self.sell_price,
                           battle_field, pos)


TOWER_TYPES = {
               "ARCHER": AttackTowerFactory("ARCHER",
                                            states={
                                                    "default": 1,
                                                    "cool_down": 4,
                                                    "attack": 3
                                                   },
                                            act_range=275, dmg=50,
                                            price=500, sell_price=400),
               "MINIGUN": AttackTowerFactory("MINIGUN",
                                             states={
                                                     "default": 1,
                                                     "cool_down": 3,
                                                     "attack": 2
                                                    },
                                             act_range=200, dmg=25,
                                             price=250, sell_price=100),
               "TANK": AttackTowerFactory("TANK",
                                          states={
                                                  "default": 1,
                                                  "cool_down": 7,
                                                  "attack": 5
                                                 },
                                          act_range=350, dmg=100,
                                          price=700, sell_price=500)
              }
