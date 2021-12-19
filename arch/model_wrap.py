import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import model.battle_field as battle_field
import loader.lvl_loader as lvl_loader
import visual.visualizer as visualizer
import model.towers as towers
import pygame as pg


class ModelWrap(base_arch.EventManager.Employee,
                vis_arch.Canvas.DrawableObj):
    '''
    Class of the model wrapper
    '''

    # Messages for model wrapper

    class BUY_TOWER(base_arch.Msg):
        '''
        Class of BUY_TOWER message for model wrapper
        '''
        '''
        Класс BUY_TOWER сообщения для обертки модели
        '''

        def __init__(self, tower_type, pos, sender=None, address=None):
            '''
            Init method for a BUT_TOWER message object
            :param tower_type: TowerTypes enum, type of the bought tower
            :param pos: (x, y) list-like object, position where
                        bought tower should be placed
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации BUY_TOWER сообщения
            :param tower_type: TowerTypes enum, тип куплленой башни
            :param pos: (x, y) list-like object, координаты, места
                        установки башни
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''

            content = {"tower-type": tower_type, "pos": pos}
            super().__init__(content, sender, address)

    class SELL_TOWER(base_arch.Msg):
        '''
        Class of SELL_TOWER message for model wrapper
        '''
        '''
        Класс SELL_TOWER сообщения для обертки модели
        '''

        def __init__(self, pos, sender=None, address=None):
            '''
            Init method for a SELL_TOWER message object
            :param pos: (x, y) list-like object, position where
                        sold tower is placed
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации SELL_TOWER сообщения
            :param pos: (x, y) list-like object, координаты, места
                        проданной  башни
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''

            content = {"pos": pos}
            super().__init__(content, sender, address)

    def __init__(self, event_manager, visual_manager, game_section, lvl_path):
        '''
        Init method of the model wrapper
        :param event_manager: event manager that will manage this
                              model wrapper
        :param visual_manager: visual manager that will manage this
                               model wrapper
        :param game_section: game section that owns this model wrapper
        :param lvl_path: path str to the level folder
        '''
        '''
        Метод иницализации обертки модели
        :param event_manager: менеджер событий, управляющий данным
                              объектом обертки
        :param visual_manager: холст, на котором будет отрисован
                               данный объект обертки
        :param game_section: игровая секция, к которой относится
                     данный объект обертки
        :param lvl_path: строка с путем до папки с уровнем
        '''

        base_arch.EventManager.Employee.__init__(self, event_manager)
        vis_arch.Canvas.DrawableObj.__init__(self, visual_manager, (280, 20))
        self.game_section = game_section
        self.clock = base_arch.Clock(self.event_manager,
                                     self.event_manager.clock, 3)
        self.clock.play()

        map_load = lvl_loader.load_map(lvl_path + "/map.png")
        tower_space, enemy_path, background = map_load
        waves = lvl_loader.load_waves(lvl_path + "/waves.json")

        self.model = battle_field.BattleField(5, tower_space,
                                              waves, enemy_path)

        self.visualizer = visualizer.Visualizer(size=(1000, 1000),
                                                background=background,
                                                battle_field=self.model)
        self.selected_tower_type = None

    def draw(self):
        '''
        Method that draws the model
        '''
        '''
        Метод, отрисовывающий модель на холсте
        '''

        self.visualizer.draw()
        sprite = pg.transform.smoothscale(self.visualizer.surf, (700, 700))
        self.visual_manager.surf.blit(sprite, self.pos)

    def run(self):
        '''
        Method that describes model default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение модели
        '''

        self.visualizer.update()
        running = self.model.update(self.clock.get_tick())
        if not running:
            win_flag = self.model.base_hp > 0
            self.game_section.end_game(win_flag)

    def call(self, msg):
        '''
        Method that describes model reaction to msg
        :param msg: message the model will react to
        '''
        '''
        Метод, описывающий реакциию модели на полученное
        сообщение
        :param msg: сообщение, отправленное модели
        '''

        base_arch.EventManager.Employee.call(self, msg)

        if isinstance(msg, ModelWrap.BUY_TOWER):
            if msg.address is self:
                tower_type = msg.content["tower-type"]
                pos = msg.content["pos"]

                real_tower_type = towers.TOWER_TYPES[tower_type]
                pos[0] = (pos[0] - self.pos[0]) / 700 * 1000
                pos[1] = (pos[1] - self.pos[1]) / 700 * 1000

                self.model.buy_tower(pos, real_tower_type)

        elif isinstance(msg, ModelWrap.SELL_TOWER):
            if msg.address is self:
                pos = msg.content["pos"]

                pos[0] = (pos[0] - self.pos[0]) / 700 * 1000
                pos[1] = (pos[1] - self.pos[1]) / 700 * 1000

                self.model.sell_tower(pos)

    def get_free_space(self, tower_type):
        '''
        Method that returns possible position for
        towers of the given type
        :param tower_type: tower type to check possible position for
        '''
        '''
        Метод, возращающий возможное положение для башен
        данного типа
        :param tower_type: тип башен, для которого нужно проверить
                           возможное положение
        '''

        real_tower_type = towers.TOWER_TYPES[tower_type]
        free_space = self.model.get_free_space(real_tower_type)
        self.selected_tower_type = tower_type
        for place in free_space:
            place[0] = place[0] * 700 / 1000 + self.pos[0]
            place[1] = place[1] * 700 / 1000 + self.pos[1]

        return free_space

    def get_occupied_space(self):
        '''
        Method that returns list of positions occupied by towers
        '''
        '''
        Метод, возращающий список мест, заннятых башнями
        '''

        occupied_space = self.model.get_occupied_space()
        for place in occupied_space:
            place[0] = place[0] * 700 / 1000 + self.pos[0]
            place[1] = place[1] * 700 / 1000 + self.pos[1]

        return occupied_space

    def get_wave(self):
        '''
        Method that returns wave description
        (current wave number, max wave number)
        '''
        '''
        Метод, возвращающий характеристику волны
        (номер текущей волны, номер последней волны)
        '''

        return self.model.get_wave_data()

    def get_money(self):
        '''
        Method that returns current money amount
        '''
        '''
        Метод, возвращающий текущее кол-во денег
        '''

        return self.model.money

    def get_base_health(self):
        '''
        Method that returns current base health
        '''
        '''
        Метод, возвращающий текущее кол-во здоровья базы
        '''

        return (self.model.base_hp, self.model.max_base_hp)
