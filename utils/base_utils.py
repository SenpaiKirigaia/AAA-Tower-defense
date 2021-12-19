import enum


class Bar:
    '''
    Class of numeric variable with lower and upper bound
    '''
    '''
    Класс числовой переменной, ограниченной сверху и снизу
    '''

    class MaxValue:
        def set_name(self, owner, name):
            self.publc_name = "max_" + name
            self.private_name = "_max_" + name

        def __get__(self, obj, objtype=None):
            return getattr(obj, self.private_name)

    class MinValue:
        def set_name(self, owner, name):
            self.publc_name = "min_" + name
            self.private_name = "_min_" + name

        def __get__(self, obj, objtype=None):
            return getattr(obj, self.private_name)

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

        max_attr = Bar.MaxValue()
        min_attr = Bar.MinValue()

        max_attr.set_name(owner, name)
        min_attr.set_name(owner, name)

        setattr(owner, "max_" + name, max_attr)
        setattr(owner, "min_" + name, min_attr)

    def __set__(self, obj, value):
        if not hasattr(obj, self.private_name):
            setattr(obj, "_max_" + self.public_name, 0)
            setattr(obj, "_min_" + self.public_name, 0)
            setattr(obj, self.private_name, 0)

        if type(value) == tuple and len(value) == 3:
            min_value = value[0]
            max_value = value[2]
            init_value = value[1]

            setattr(obj, "_max_" + self.public_name, max_value)
            setattr(obj, "_min_" + self.public_name, min_value)

            init_value = max(init_value, min_value)
            init_value = min(init_value, max_value)

            setattr(obj, self.private_name, init_value)

        elif type(value) in (int, float):
            max_attr = getattr(obj, "_max_" + self.public_name)
            min_attr = getattr(obj, "_min_" + self.public_name)

            value = max(value, min_attr)
            value = min(value, max_attr)

            setattr(obj, self.private_name, value)

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)


class SafeIter:
    '''
    Class of safe iterator
    (iterator that cannot go beyond the limits)
    '''
    '''
    Класс безопасного итератора
    (Итератор, который не может выйти за пределы)
    '''

    indx = Bar()

    def __init__(self, iterable):
        '''
        Init method of safe itarator
        :param iterable: base iterable object
        '''
        '''
        Метод инициализации безопасного итератора
        :param iterable: базовы итерабельный объект
        '''

        self.iterable = iterable
        self.length = len(iterable)
        self.indx = (0, 0, self.length - 1)

    def prev(self):
        '''
        Method that moves pointer to previous slot
        '''
        '''
        Метод, передвигающей указатель в предыдущую ячейку
        '''

        self.indx -= 1
        return self.current()

    def next(self):
        '''
        Method that moves pointer to next slot
        '''
        '''
        Метод, передвигающей указатель в следющую ячейку
        '''

        self.indx += 1
        return self.current()

    def current(self):
        '''
        Method that returns element at current position
        '''
        '''
        Метод, возвращающий элемент на текущей позиции указателя
        '''

        if self.indx < self.length:
            return self.iterable[self.indx]
        else:
            return None

    def at_end(self):
        '''
        Method that checks if pointer at the end
        '''
        '''
        Метод, проверяющий достижение указателем конца
        '''

        return self.indx == self.length - 1

    def at_start(self):
        '''
        Method that checks if pointer at the start
        '''
        '''
        Метод, проверяющий достижение указателем начала
        '''

        return self.indx == 0


class Timer:
    '''
    Class of the timer
    '''
    '''
    Класс таймера
    '''

    time = Bar()

    def __init__(self, time):
        '''
        Init method of the timer
        :param time: time limit of the timer
        '''
        '''
        Метод инциализации таймера
        :param time: засеченное время
        '''

        self.time = (0, 0, time)

    def reset(self, time=0):
        '''
        Method that resets the timer
        :param time: new time limit of the timer,
                     default value = 0 - time limit
                     will not be changed
        '''
        '''
        Метод, перезапускающий таймер
        :param time: новое засеченное время,
                     дефолтное значение = 0 - засеченное время
                     не изменится
        '''

        if time > 0:
            self.time = (0, 0, time)
        else:
            self.time = 0

    def is_ringing(self):
        '''
        Method that checks if the timer is ringing
        '''
        '''
        Метод, проверяющий звонит ли таймер
        '''

        return self.time == self.max_time

    def update(self, dt):
        '''
        Method that updates the timer
        :param dt: passed time
        '''
        '''
        Метод, обнавляющий таймер
        :param dt: прощедшее время
        '''

        self.time += dt


class DIR(enum.Flag):
    '''
    Direction enumeration
    '''
    '''
    Enum направления
    '''
    E = enum.auto()
    S = enum.auto()
    W = enum.auto()
    N = enum.auto()


def vec_norm(x, y):
    '''
    Function that normalize the vector
    :param x: x - vector coordinate
    :param y: y - vector coordinate
    '''
    '''
    Функция, нормализующая вектор
    :param x: x - координата вектора
    :param y: y - координата вектора
    '''

    length = (x**2 + y**2)**0.5

    if length == 0:
        return 0, 0

    n_x = x / length
    n_y = y / length

    return n_x, n_y
