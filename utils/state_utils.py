import utils.base_utils as base_utils


class State(base_utils.Timer):
    '''
    Class of the state
    '''
    '''
    Класс состояния
    '''

    def __init__(self, name, time):
        '''
        Init method of the state instance
        :param name: name of the state
        :param time: duration of the state
        '''
        self.name = name
        super().__init__(time)


class StateLib:
    '''
    Class of state collection
    '''
    '''
    Класс сборника состояний
    '''
    class NameDecor:
        def __init__(self, owner):
            self.owner = owner

        def __getattr__(self, attr_name):
            getattr(self.owner, attr_name)
            return attr_name

    def __init__(self, states):
        '''
        Init method of state collection
        :param states: {name: duration} - dict of states
        '''
        '''
        Метод инициализации сборника состояний
        :param states: {название состояния: длительность состояния}
                       - словарь стояний
        '''

        names = StateLib.NameDecor(self)
        self.names = names
        for name, duration in states.items():
            setattr(self, f"{name}", self.gen_state_func(name, duration))

    def gen_state_func(self, name, duration):
        return lambda: State(name, duration)
