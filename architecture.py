import pygame as pg


class Msg:
    '''
    Class of a message
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
        self.content = content
        self.sender = sender
        self.address = address


class PyGameMsg:
    '''
    Wrapper for pygame event
    '''

    def __init__(self, pg_event):
        '''
        Init method for a pygame event wrapper message
        :params pg_event: pygame event to wrap
        '''
        content = {
                    'event_args': pg_event.__dict__,
                    'event_type': pg_event.type
                  }
        super().__init__(content=content)


class Manager:
    '''
    Class of a manager
    All types of manager classes should be inherited from it
    '''

    # Messages for Manager object

    class ADD_OBJ(Msg):
        '''
        Class of ADD_OBJ message for Manager
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
            content = {"target": target}
            super().__init__(content, sender, address)

    class REMOVE_OBJ(Msg):
        '''
        Class of REMOVED_OBJ message for Manager
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
            content = {"target": target}
            super().__init__(content, sender, address)

    def __init__(self):
        '''
        Init method for a Manager object
        '''
        self.employees = []

    def call(self, msg):
        '''
        Method that describes Manager reaction to msg
        :param msg: message the Manager will react to
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

        pass


class BaseEventManager(Manager):
    '''
    Class of an base event manager
    '''

    class Employee:
        '''
        Class of employee object event manager can manage
        '''

        def __init__(self, event_manager):
            '''
            Init method for employee
            :param event_manager: event manager that will manage
                                  this employee
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

            pass

        def run(self):
            '''
            Method that describes Employee default behaviour
            '''

            pass

    def __init__(self):
        '''
        Init method of a base event manager
        '''
        super().__init__()
        self.msg_queue = []

    def run(self):
        '''
        Method that describes base event manager default behaviour
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

        self.queue.append(msg)


class EventManager(BaseEventManager, BaseEventManager.Employee):
    '''
    Subclass of BaseEventManager that can be managed by another
    event manager
    '''

    def __init__(self, event_manager):
        '''
        Init method of a event manager
        :param event_manager: event manager that will manage
                              this event manager

        '''
        self.clock = Clock(self, event_manager.clock)
        BaseEventManager.__init__(self)
        BaseEventManager.Employee__init__(self, event_manager)

    def run(self):
        '''
        Method that describes event manager default behaviour
        '''
        BaseEventManager.run(self)

    def call(self, msg):
        '''
        Method that describes event manager reaction to msg
        :param msg: message the event manager will react to
        '''
        BaseEventManager.call(self, msg)


class MasterEventManager(BaseEventManager):
    '''
    class of master event manager
    '''

    def __init__(self, FPS):
        '''
        Init method of a master event manager
        :param FPS: FPS of the program
        '''

        self.running = True
        self.clock = MasterClock(self, FPS)
        super().__init__()

    def run(self):
        '''
        Method that describes MasterEventManager default behaviour
        '''

        for event in pg.get_event():
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

        if isinstance(msg, PyGameMsg):
            if msg.content["type"] == pg.QUIT:
                self.running = False

        else:
            super().call(msg)


class Clock(Manager, EventManager.Employee):
    '''
    Class of a clock(time manager)
    '''

    def __init__(self, event_manager, base_clock, scale=1):
        '''
        Init method of a clock
        :param event_manager: event manager that will manage this clock
        :param base_clock: base clock that will manage this clock
        :param scale: scale of clock, i.e how many
                      seconds will pass per one real second

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

        if self.running:
            for employee in self.employees:
                employee.update(self.dt)

    def update(self, dt):
        '''
        Method that updates the clock
        :param dt: dt of the base clock
        '''

        if self.running:
            self.dt = self.scale * dt
            self.current_time += self.dt

    def get_time(self):
        '''
        Method that returns passed time
        '''

        return self.current_time

    def get_tick(self):
        '''
        Method that returns last dt
        '''

        return self.dt

    def play(self):
        '''
        Method that activates the clock
        '''

        self.running = True

    def pause(self):
        '''
        Method that pauses the clock
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

    class DrawableObj:
        '''
        Class of a drawable object
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
            self.visual_manager
            add_msg = Manager.ADD_OBJ(target=self,
                                      address=visual_manager)
            visual_manager.event_manager.post(add_msg)

        def draw(self):
            '''
            Method that draws the object
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

        self.size = size
        self.surf = pg.Surface(self.size, pg.SRCALPHA)
        self.bg_color = bg_color

        Manager.__init__(self)
        EventManager.Employee.__init__(self, event_manager)

    def run(self):
        '''
        Method that describes base visual manager default behaviour
        '''

        self.surf.fill(self.bg_color)
        for employee in self.employees:
            employee.draw()


class Canvas(BaseCanvas, BaseCanvas.DrawableObj):
    '''
    Subclass of BaseCanvas that can be managed
    by another visual manager
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

    def __init__(self, event_manager, size, bg_color=(255, 255, 255, 0)):
        '''
        Init method of the master canvas
        :param event_manager: event manager that will manage this
                              canvas
        :param size: list with the size of the canvas (size of the window)
        :param bg_color: background color of the canvas
        '''

        super().__init__(event_manager, size, bg_color)
        self.surf = pg.display.set_mode(self.size)

    def run(self):
        '''
        Method that describes base visual manager default behaviour
        '''

        super().run()
        pg.display.update()
