import pygame as pg
import visual.animas as animas


class Visualizer:
    '''
    Class of model visualizer
    '''
    '''
    Класс визуализатора модели
    '''

    def __init__(self, size, background, battle_field):
        '''
        Init method of the visualizer
        :param size: [width, height] - size of the visualization
        :param background: background of the visualization
        :param battle_field: link to the current game environment
        '''
        '''
        Метод инициализации визуализатора
        :param size: [width, height] - размеры визуализации
        :param background: задний фон визуализации
        :param battle_field: ссылка на текущее игровое окружения
        '''

        self.size = size
        self.surf = pg.Surface(self.size, pg.SRCALPHA)
        self.background = background
        self.battle_field = battle_field

        self.animas = []

    def draw(self):
        '''
        Method that creates the visualization
        '''
        '''
        Метод, создающий визуализацию
        '''

        if type(self.background) == tuple:
            self.surf.fill(self.background)
        elif type(self.background) == pg.Surface:
            self.surf.blit(self.background, (0, 0))
        pg.draw.rect(self.surf, (253, 244, 37), pg.Rect((0, 0), self.size),
                     width=3)

        for anima in self.animas:
            anima.draw()

    def update(self):
        '''
        Method that updates the visualization
        '''
        '''
        Метод, обновляющий визуализацию
        '''

        for obj in self.battle_field.fresh_objs:
            anima_factory = animas.ANIMAS_FACTORIES[obj.type_name]
            anima = anima_factory.get_anima(self.surf, obj)
            self.animas.append(anima)

        del_animas = []
        for anima in self.animas:
            if anima.obj in self.battle_field.del_objs:
                del_animas.append(anima)

        self.battle_field.fresh_objs.clear()
        self.battle_field.del_objs.clear()

        for anima in del_animas:
            self.animas.remove(anima)
