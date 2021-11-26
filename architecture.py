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
            if msg.content["target"] not in self.employees:
                self.employees.append(msg.content["target"])

        elif isinstance(msg, Manager.REMOVE_OBJ):
            if msg.content["target"] in self.employees:
                self.employees.remove(msg.content["target"])

    def run(self):
        '''
        Method that describes Manager default behaviour
        '''

        pass


class EventManager(Manager):
    '''
    Class of an event manager
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

    def __init__(self, event_manager=None):
        '''
        Init method of a event manager
        '''
        super().__init__()
        self.msg_queue = []
        self.event_manager = event_manager

        if self.event_manager is not None:
            add_msg = Manager.ADD_OBJ(target=self,
                                      address=self.event_manager)
            self.event_manager.post(add_msg)

    def run(self):
        '''
        Method that describes EventManager default behaviour
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


class MasterEventManager(EventManager):
    '''
    class of master event manager
    '''

    def __init__(self):
        '''
        Init method of a master event manager
        '''

        self.running = True
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
