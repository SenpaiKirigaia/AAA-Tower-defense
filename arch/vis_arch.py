import pygame as pg
import arch.base_arch as base_arch


class BaseCanvas(base_arch.Manager, base_arch.EventManager.Employee):
    '''

    Class of a base canvas (base visual manager)
    '''
    '''
    Класс базового холста (базовый менеджер отрисовки)
    '''

    # Messages for BaseCanvas object

    class SET_GUI(base_arch.Msg):
        '''
        Class of SET_GUI message for Manager
        '''
        '''
        Класс SET_GUI сообщения для менеджера
        '''

        def __init__(self, target, sender=None, address=None):
            '''
            Init method for a SET_GUI message object
            :param target: link to the GUI object
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации SET_GUI сообщения
            :param target: ссылка на объект графческого пользовательского
                           интерфейса
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''
            content = {"target": target}
            super().__init__(content, sender, address)

    # Employees of BaseCanvas object

    class DrawableObj:
        '''
        Class of a drawable object
        '''
        '''
        Класс объекта, который может быть отрисован на холсте
        '''

        def __init__(self, visual_manager, pos):
            '''
            Init method of the drawable object
            :param visual_manager: visual manager that will
                                   manage this drawable
                                   object
            :param pos: list with the position of top left
                        corner of the drawable object
            '''
            '''
            Метод инциализия рисуемого объекта
            :param visual_manager: холст, на котором будет отрисован
                                   данный объект
            :param pos: список с координатами левого верхнего угла
                        рисуемого объекта

            '''
            self.visual_manager = visual_manager
            self.pos = pos
            add_msg = BaseCanvas.ADD_OBJ(target=self,
                                         address=visual_manager)
            visual_manager.event_manager.post(add_msg)

        def draw(self):
            '''
            Method that draws the object
            '''
            '''
            Метод, отрисовывающий объект на холсте
            '''

            pass

    def __init__(self, event_manager, size, bg_color=(255, 255, 255, 0)):
        '''
        Init method of the base canvas
        :param event_manager: event manager that will manage this
                              canvas
        :param size: list with the size of the canvas
        :param bg_color: background color of the canvas
        '''
        '''
        Метод иницализации базового холста
        :param event_manager: менеджер событий, управляющий данным
                              холсто
        :param size: список с размерами холста
        :param bg_color: фоновый цвет холоста
        '''

        self.size = size
        self.surf = pg.Surface(self.size, pg.SRCALPHA)
        self.bg_color = bg_color
        self.gui = None

        base_arch.Manager.__init__(self)
        base_arch.EventManager.Employee.__init__(self, event_manager)

    def call(self, msg):
        '''
        Method that describes base canvas reaction to msg
        :param msg: message the base canvas will react to
        '''
        '''
        Метод, описывающий реакциию базового холста на полученное
        сообщение
        :param msg: сообщение, отправленное базовому холсту
        '''

        base_arch.Manager.call(self, msg)
        if isinstance(msg, BaseCanvas.SET_GUI):
            if msg.address is self:
                self.gui = msg.content["target"]

    def run(self):
        '''
        Method that describes base visual manager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение холста
        '''

        self.surf.fill(self.bg_color)
        for employee in self.employees:
            employee.draw()

        if self.gui is not None:
            self.gui.draw()


class Canvas(BaseCanvas, BaseCanvas.DrawableObj):
    '''
    Subclass of BaseCanvas that can be managed
    by another visual manager
    '''
    '''
    Подкласс базового холста, который может отрисовываться на другом
    холсте
    '''

    def __init__(self, event_manager, visual_manager, size, pos,
                 bg_color=(255, 255, 255, 0)):
        '''
        Init method of the canvas
        :param event_manager: event manager that will manage this
                              canvas
        :param visual_manager: visual manager that will manage this
                               canvas
        :param size: list with the size of the canvas
        :param pos: list with the position of top left
                   corner of the canvas
        :param bg_color: background color of the canvas
        '''
        '''
        Метод иницализации холста
        :param event_manager: менеджер событий, управляющий данным
                              холсто
        :param visual_manager: холст, на котором будет отрисован
                               данный холст
        :param size: список с размерами холста
        :param pos: список с координатами левого верхнего угла
                    холста
        :param bg_color: фоновый цвет холоста
        '''

        BaseCanvas.__init__(self, event_manager, size, bg_color)
        BaseCanvas.DrawableObj.__init__(self, visual_manager, pos)
        if isinstance(self.visual_manager, MasterCanvas):
            self.master_canvas = self.visual_manager
        else:
            self.master_canvas = self.visual_manager.master_canvas

    def draw(self):
        '''
        Method that draws the canvas
        '''

        self.visual_manager.surf.blit(self.surf, self.pos)


class MasterCanvas(BaseCanvas):
    '''
    Class of master canvas (main surface of whole app)
    '''
    '''
    Класс главного холста всего приложения
    '''

    def __init__(self, event_manager, size, bg_color=(255, 255, 255, 0)):
        '''
        Init method of the master canvas
        :param event_manager: event manager that will manage this
                              canvas
        :param size: list with the size of the canvas (size of the window)
        :param bg_color: background color of the canvas
        '''
        '''
        Метод иницализации главного холста
        :param event_manager: менеджер событий, управляющий данным
                              холсто
        :param size: список с размерами холста (размеры окна)
        :param bg_color: фоновый цвет холоста
        '''

        super().__init__(event_manager, size, bg_color)
        self.surf = pg.display.set_mode(self.size)

    def run(self):
        '''
        Method that describes master visual manager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение главного холста
        '''

        super().run()
        pg.display.update()
