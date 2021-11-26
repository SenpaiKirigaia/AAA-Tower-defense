

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


class Manager():
    '''
    Class of a manager
    All types of manager classes should be inherited from it
    '''

    # Messages for Manager object

    class ADD_OBJ(Msg):
        '''
        class of ADD_OBJ message for Manager
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
        class of REMOVED_OBJ message for Manager
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
