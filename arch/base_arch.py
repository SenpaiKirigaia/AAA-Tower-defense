import pygame as pg


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


class PyGameMsg(Msg):
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
        super().__init__(content)


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

        def __init__(self, target, sender=None, address=None):
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

        def __init__(self, target, sender=None, address=None):
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
    # Messages for event manager

    class TRANS_MSG(Msg):
        '''
        Class of TRANS_MSG message for base event manager
        '''
        '''
        Класс TRANS_MSG сообщения для базвого обработчика событий
        '''

        def __init__(self, sub_msg, sender=None, address=None):
            '''
            Init method for a TRANS_MSG message object
            :param sub_msg: link to the message to be transported
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            :param address: link to the addressee of the message,
                            default value is None (message wil be delivered
                            to all local objects)
            '''
            '''
            Метод инциалиации TRANS_MSG сообщения
            :param sub_msg: ссылка на письмо, которое нужно передать
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            :param address: ссылка на получателя сообщения,
                            дефолтное значение - None(сообщение будет
                            доставленно всем локальным объектам)
            '''

            content = {"sub_msg": sub_msg}
            super().__init__(content, sender, address)

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

            add_msg = Manager.ADD_OBJ(self, address=self.event_manager,
                                      sender=self)
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

        while self.msg_queue:
            msg = self.msg_queue.pop(0)
            self.call(msg)
            for employee in self.employees:
                employee.call(msg)

        for employee in self.employees:
            employee.run()

    def call(self, msg):
        '''
        Method that describes base event manager reaction to msg
        :param msg: message the base event manager will react to
        '''
        '''
        Метод, описывающий реакциию базовго обработчика событий на полученное
        сообщение
        :param msg: сообщение, отправленное базовому обработчику событий
        '''

        super().call(msg)
        if isinstance(msg, BaseEventManager.TRANS_MSG):
            if msg.sender is not self:
                self.post(msg.content["sub_msg"])

                if msg.address is not self:
                    sub_msg = msg.content["sub_msg"]
                    address = msg.address

                    new_msg = BaseEventManager.TRANS_MSG(sub_msg, self,
                                                         address)
                    self.post(new_msg)

    def post(self, msg):
        '''
        Method that adds msg to the message queue
        :param msg: message to be posted
        '''
        '''
        Метод, добавляющий сообщение в очередь сообщений
        :param msg:
        '''

        self.msg_queue.append(msg)


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

        BaseEventManager.__init__(self)
        BaseEventManager.Employee.__init__(self, event_manager)
        self.clock = Clock(self, event_manager.clock)
        self.clock.play()

        if isinstance(self.event_manager, MasterEventManager):
            self.master_manager = self.event_manager
        else:
            self.master_manager = self.event_manager.master_manager

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

    # Messages for master event manager

    class QUIT(Msg):
        '''
        Class of QUIT message for master event manager
        '''
        '''
        Класс QUIT сообщения для главного обработчика событий
        '''

        def __init__(self, sender=None):
            '''
            Init method for a QUIT message object
            :param sender: link to the sender of the message,
                           default value is None (anonymous message)
            '''
            '''
            Метод инциалиации QUIT сообщения
            :param sender:  ссылка на отправителя сообщения,
                            дефолтное значение - None(анонимное сообщение)
            '''

            super().__init__(sender=sender)

    def __init__(self, FPS):
        '''
        Init method of a master event manager
        :param FPS: FPS of the program
        '''
        '''
        Метод инициализации главного обработчика событий
        :param FPS: FPS программы
        '''

        super().__init__()
        self.running = True
        self.clock = MasterClock(self, FPS)

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
            self.post(msg)
            self.post(MasterEventManager.TRANS_MSG(msg, self))

        super().run()

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

        super().call(msg)
        if isinstance(msg, PyGameMsg):
            if msg.content["event"].type == pg.QUIT:
                self.running = False

        elif isinstance(msg, MasterEventManager.QUIT):
            self.running = False


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
        EventManager.Employee.__init__(self, event_manager)

    def run(self):
        '''
        Method that describes master clock default behaviour
        '''

        self.dt = self.pg_clock.tick(self.FPS) / 1000
        self.current_time += self.dt
        for employee in self.employees:
            employee.update(self.dt)

    def get_time(self):
        '''
        Method that returns passed time
        '''

        return self.current_time
