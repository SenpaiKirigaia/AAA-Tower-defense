import pygame as pg
import pygame_gui as pg_gui


class Msg:
    '''
    Class of a message
    '''
    '''
    Класс сообщений
    '''

    def __init__(self, content=dict(), sender=None, address=None):
        '''
        Init method for a message object
        :param content: dictionary with the content of the message
        :param sender: link to the sender of the message,
                       default value is None (anonymous message)
        :param address: link to the addressee of the message,
                        default value is None (message wil be delivered
                        to all local objects)
        '''
        '''
        Инициализирующий метод объекта сообщения
        :param content: словарь с содержанием сообщения
        :param sender:  ссылка на отправителя сообщения,
                        дефолтное значение - None(анонимное сообщение)
        :param address: ссылка на получателя сообщения,
                        дефолтное значение - None(сообщение будет доставленно
                        всем локальным объектам)

        '''
        self.content = content
        self.sender = sender
        self.address = address


class PyGameMsg:
    '''
    Wrapper for pygame event
    '''
    '''
    Обертка для pygame event в виде сообщения
    '''

    def __init__(self, pg_event):
        '''
        Init method for a pygame event wrapper message
        :params pg_event: pygame event to wrap
        '''
        '''
        Метод инициализации сообщения, оборочивающего pygame event
        :param pg_event: pygame event, который нужно обернуть
        '''
        content = {
                    'event': pg_event
                  }
        super().__init__(content=content)


class Manager:
    '''
    Class of a manager
    All types of manager classes should be inherited from it
    '''
    '''
    Класс менеджеров
    Все типы менеджеров должны быть унаследованы от этого класса
    '''

    # Messages for Manager object

    class ADD_OBJ(Msg):
        '''
        Class of ADD_OBJ message for Manager
        '''
        '''
        Класс ADD_OBJ сообщения для менеджера
        '''

        def __init__(target, sender=None, address=None):
            '''
            Init method for a ADD_OBJ message object
            :param target: link to the object to be added to
                           the manager employees list
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации ADD_OBJ сообщения
            :param target: ссылка на объект, который нужно добавить
                           в список рабочих менеджера
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''
            content = {"target": target}
            super().__init__(content, sender, address)

    class REMOVE_OBJ(Msg):
        '''
        Class of REMOVED_OBJ message for Manager
        '''
        '''
        Класс REMOVE_OBJ сообщения для менеджера
        '''

        def __init__(target, sender=None, address=None):
            '''
            Init method for a REMOVED_OBJ message object
            :param target: link to the object to be removed from
                           the manager employees list
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации REMOVE_OBJ сообщения
            :param target: ссылка на объект, который нужно удалить
                           из списка рабочих менеджера
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''
            content = {"target": target}
            super().__init__(content, sender, address)

    def __init__(self):
        '''
        Init method for a Manager object
        '''
        '''
        Метод инициализации менеджера
        '''
        self.employees = []

    def call(self, msg):
        '''
        Method that describes Manager reaction to msg
        :param msg: message the Manager will react to
        '''
        '''
        Метод, описывающий реакциию Менеджера на полученное
        сообщение
        :param msg: сообщение, отправленное менеджеру
        '''

        if isinstance(msg, Manager.ADD_OBJ):
            if msg.address is self:
                if msg.content["target"] not in self.employees:
                    self.employees.append(msg.content["target"])

        elif isinstance(msg, Manager.REMOVE_OBJ):
            if msg.address is self:
                if msg.content["target"] in self.employees:
                    self.employees.remove(msg.content["target"])

    def run(self):
        '''
        Method that describes Manager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение Менеджера
        '''

        pass


class BaseEventManager(Manager):
    '''
    Class of an base event manager
    '''
    '''
    Базовый класс обработчик событий
    '''

    class Employee:
        '''
        Class of employee object event manager can manage
        '''
        '''
        Класс работника, которым может управлять менеджер событий
        '''

        def __init__(self, event_manager):
            '''
            Init method for employee
            :param event_manager: event manager that will manage
                                  this employee
            '''
            '''
            Метод инициализации работника
            :param event_manager: обработчик событий, управляющий данным
                                  объектом
            '''

            self.event_manager = event_manager

            add_msg = Manager.ADD_OBJ(target=self,
                                      address=self.event_manager)
            self.event_manager.post(add_msg)

        def call(self, msg):
            '''
            Method that describes Employee reaction to msg
            :param msg: message the Employee will react to
            '''
            '''
            Метод, описывающий реакциию Работника на полученное
            сообщение
            :param msg: сообщение, отправленное работнику
            '''

            pass

        def run(self):
            '''
            Method that describes Employee default behaviour
            '''
            '''
            Метод, описывающий дефолтное поведение работника
            '''

            pass

    def __init__(self):
        '''
        Init method of a base event manager
        Метод инициализиции базового обработчика событий
        '''
        super().__init__()
        self.msg_queue = []

    def run(self):
        '''
        Method that describes base event manager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение базового обработчика
        событий
        '''

        for msg in self.msg_queue:
            if msg.address is self:
                self.call(msg)
            for employee in self.employees:
                employee.call(msg)

        for employee in self.employees:
            employee.run()

    def post(self, msg):
        '''
        Method that adds msg to the message queue
        :param msg: message to be posted
        '''
        '''
        Метод, добавляющий сообщение в очередь сообщений
        :param msg:
        '''

        self.queue.append(msg)


class EventManager(BaseEventManager, BaseEventManager.Employee):
    '''
    Subclass of BaseEventManager that can be managed by another
    event manager
    '''
    '''
    Подкласс базового обработчика событий, которым может управлять
    другой обработчик событий
    '''

    def __init__(self, event_manager):
        '''
        Init method of a event manager
        :param event_manager: event manager that will manage
                              this event manager

        '''
        '''
        Метод инициализации обработчика событий
        :param event_manager: обработчик событий, управляющий данным
                              объектом
        '''

        self.clock = Clock(self, event_manager.clock)
        BaseEventManager.__init__(self)
        BaseEventManager.Employee__init__(self, event_manager)

    def run(self):
        '''
        Method that describes event manager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение обработчика
        событий
        '''

        BaseEventManager.run(self)

    def call(self, msg):
        '''
        Method that describes event manager reaction to msg
        :param msg: message the event manager will react to
        '''
        '''
        Метод, описывающий реакциию обработчика событий на полученное
        сообщение
        :param msg: сообщение, отправленное обработчику событий
        '''

        BaseEventManager.call(self, msg)


class MasterEventManager(BaseEventManager):
    '''
    Class of master event manager
    '''
    '''
    Класс главного обработчика событий
    '''

    def __init__(self, FPS):
        '''
        Init method of a master event manager
        :param FPS: FPS of the program
        '''
        '''
        Метод инициализации главного обработчика событий
        :param FPS: FPS программы
        '''

        self.running = True
        self.clock = MasterClock(self, FPS)
        super().__init__()

    def run(self):
        '''
        Method that describes MasterEventManager default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение главно обработчика
        событий
        '''

        for event in pg.event.get():
            msg = PyGameMsg(event)
            self.call(msg)
            for employee in self.employee:
                employee.call(msg)

        for employee in self.employees:
            employee.run()

        return self.running

    def call(self, msg):
        '''
        Method that describes MasterEventManager reaction to msg
        :param msg: message the MasterEventManager will react to
        '''
        '''
        Метод, описывающий реакциию главного обработчика событий на полученное
        сообщение
        :param msg: сообщение, отправленное главному обработчику событий
        '''

        if isinstance(msg, PyGameMsg):
            if msg.content["event"].type == pg.QUIT:
                self.running = False

        else:
            super().call(msg)


class Clock(Manager, EventManager.Employee):
    '''
    Class of a clock(time manager)
    '''
    '''
    Класс часов(менеджера времени)
    '''

    def __init__(self, event_manager, base_clock, scale=1):
        '''
        Init method of a clock
        :param event_manager: event manager that will manage this clock
        :param base_clock: base clock that will manage this clock
        :param scale: scale of clock, i.e how many
                      seconds will pass per one real second
        '''
        '''
        Метод инициализации часов
        :param event_manager: менеджер событий, управляющий данными
                              часами
        :param base_clock: часы, от которых будут зависеть данные часы
        :param scale: относительная скорость течения времени
        '''
        self.dt = 0
        self.running = False
        self.scale = scale
        self.current_time = 0
        self.base_clock = base_clock

        Manager.__init__(self)
        EventManager.Employee.__init__(self, event_manager)
        add_msg = Manager.ADD_OBJ(target=self,
                                  address=base_clock)
        self.base_clock.event_manager.post(add_msg)

    def run(self):
        '''
        Method that describes clock default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение часов
        '''

        if self.running:
            for employee in self.employees:
                employee.update(self.dt)

    def update(self, dt):
        '''
        Method that updates the clock
        :param dt: dt of the base clock
        '''
        '''
        Метод обновления часов
        :param dt: изменение времени часов, от которых зависят данные
                   часы
        '''

        if self.running:
            self.dt = self.scale * dt
            self.current_time += self.dt

    def get_time(self):
        '''
        Method that returns passed time
        '''
        '''
        Метод, возращающий текущее время
        '''

        return self.current_time

    def get_tick(self):
        '''
        Method that returns last dt
        '''
        '''
        Метод, возвращающий последнее изменение времени
        '''

        return self.dt

    def play(self):
        '''
        Method that activates the clock
        '''
        '''
        Метод, запускающий часы
        '''

        self.running = True

    def pause(self):
        '''
        Method that pauses the clock
        '''
        '''
        Метод, останавливающий часы
        '''

        self.running = False
        self.dt = 0

    def restart(self, init_time=0):
        '''
        Method that restarts the clock
        :param init_time: time that will be set after
                          the start, default value is 0
        '''

        self.current_time = init_time

    def change_flow(self, scale):
        '''
        Method that sets new scale of the clock
        '''

        self.scale = scale


class MasterClock(Manager, EventManager.Employee):
    '''
    Class of a master clock
    '''

    def __init__(self, event_manager, FPS):
        '''
        Init method of the master clock
        :param event_manager: event manager that will manage this
                              master clock
        :param FPS: FPS of the master clock
        '''

        self.FPS = FPS
        self.pg_clock = pg.time.Clock()
        self.current_time = 0
        Manager.__init__(self)
        EventManager.Employee(self, event_manager)

    def run(self):
        '''
        Method that describes master clock default behaviour
        '''

        self.dt = self.pg_clocl.tick(self.FPS) / 1000
        self.current += self.dt
        for employee in self.employees:
            employee.update(self.dt)

    def get_time(self):
        '''
        Method that returns passed time
        '''

        return self.current_time


class BaseCanvas(Manager, EventManager.Employee):
    '''
    Class of a base canvas (base visual manager)
    '''
    '''
    Класс базового холста (базовый менеджер отрисовки)
    '''

    # Messages for BaseCanvas object

    class SET_GUI(Msg):
        '''
        Class of ADD_OBJ message for Manager
        '''
        '''
        Класс SET_GUI сообщения для менеджера
        '''

        def __init__(target, sender=None, address=None):
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
            self.visual_manager
            add_msg = Manager.ADD_OBJ(target=self,
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

        Manager.__init__(self)
        EventManager.Employee.__init__(self, event_manager)

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

        Manager.call(self, msg)
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
        BaseCanvas.DrawableObj.__init__(self, visual_manager)

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


class GUI(EventManager.Employee):
    '''
    Class of GUI
    '''
    '''
    Класс графического пользовательского интерфейса (ГПИ)
    '''

    Button = pg_gui.elements.ui_button.UIButton
    button_events = (
                     pg_gui.UI_BUTTON_PRESSED,
                     pg_gui.UI_BUTTON_DOUBLE_CLICKED,
                     pg_gui.UI_BUTTON_ON_HOVERED,
                     pg_gui.UI_BUTTON_ON_UNHOVERED,
                    )

    def __init__(self, event_manager, visual_manager):
        '''
        Init method of the GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        '''
        '''
        Метод иницализации ГПИ
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        '''

        EventManager.Employee.__init__(self, event_manager)

        self.visual_manager = visual_manager
        add_msg = Canvas.SET_GUI(target=self, address=self.visual_manager)
        self.event_manager.post(add_msg)

        self.clock = Clock(self.event_manager, self.event_manager.clock)
        self.clock.play()

        self.ui_manager = pg_gui.UI_Manager(self.visual_manager.size)
        self.buttons = dict()

    def draw(self):
        '''
        Method that draws the GUI
        '''
        '''
        Метод, отрисовывающий ГПИ на холсте
        '''
        self.ui_manager.draw_ui(self.visual_manager.surf)

    def run(self):
        '''
        Method that describes GUI default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение ГПИ
        '''

        self.event_manager.update(self.clock.get_tick())

    def call(self, msg):
        '''
        Method that describes GUI reaction to msg
        :param msg: message the GUI will react to
        '''
        '''
        Метод, описывающий реакциию ГПИ на полученное
        сообщение
        :param msg: сообщение, отправленное ГПИ
        '''

        if isinstance(msg, PyGameMsg):
            event = msg.content['event']
            self.ui_manager.proccess_events(event)
            if event.type == pg.USEREVENT:
                if event.user_type in GUI.button_events:
                    self.button_hadling(event)

    def button_handling(self, event):
        '''
        Method for proccessing of button related events
        :param event: button related pygame event,
                      gui should proccess
        '''
        '''
        Метод, обрабатывающий события кнопок
        :param event: pygame event связанный с кнопками,
                      которое ГПИ должен обработать
        '''

        pass
