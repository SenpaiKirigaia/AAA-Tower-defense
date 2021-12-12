import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import enum


class ModelWrap(base_arch.EventManager.Employee,
                vis_arch.Canvas.DrawableObj):
    '''
    Class of the model wrapper
    '''

    class TowerTypes(enum.Enum):
        ARCHER = enum.auto()
        SUPPORT = enum.auto()

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
            Init method for a ADD_OBJ message object
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
            Метод инциалиации ADD_OBJ сообщения
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

    def __init__(self, event_manager, visual_manager):
        '''
        Init method of the model wrapper
        :param event_manager: event manager that will manage this
                              model wrapper
        :param visual_manager: visual manager that will manage this
                               model wrapper
        '''
        '''
        Метод иницализации обертки модели
        :param event_manager: менеджер событий, управляющий данным
                              объектом обертки
        :param visual_manager: холст, на котором будет отрисован
                               данный объект обертки
        '''

        base_arch.EventManager.Employee.__init__(self, event_manager)
        vis_arch.Canvas.DrawableObj.__init__(self, visual_manager, (280, 20))
        self.model = None
        self.clock = base_arch.Clock(self.event_manager,
                                     self.event_manager.clock, 3)
        self.clock.play()

    def draw(self):
        '''
        Method that draws the model
        '''
        '''
        Метод, отрисовывающий модель на холсте
        '''

        pass

    def run(self):
        '''
        Method that describes model default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение модели
        '''

        pass

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
                pass

    def get_free_space(self, tower_type):
        '''
        Method that returns possible position for
        towers of the given type
        :param tower_type: TowerTypes enum, tower type
                           to check possible position for
        '''
        '''
        Метод, возращающий возможное положение для башен
        данного типа
        :param tower_type: TowerTypes enum, тип башен,
                           для которого нужно проверить
                           возможное положение
         '''

        return [(self.pos[0] + 0, self.pos[0] + 0)]

    def get_wave(self):
        '''
        Method that returns wave description
        (current wave number, max wave number)
        '''
        '''
        Метод, возвращающий характеристику волны
        (номер текущей волны, номер последней волны)
        '''

        return (0, 0)

    def get_money(self):
        '''
        Method that returns current money amount
        '''
        '''
        Метод, возвращающий текущее кол-во денег
        '''

        return 0
