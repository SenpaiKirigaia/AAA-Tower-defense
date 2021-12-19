import model.towers as towers
import loader.sprites_loader as sprites_loader


class Anima:
    '''
    Class of animation collection
    '''
    '''
    Класс сборника анимаций
    '''

    def __init__(self, ms_surf, obj, anims):
        '''
        Init method of animation collection
        :param ms_surf: surface to blit animation on
        :param obj: obj whose state will be tracked
        :param anims: {obj.state.name : list()} - dict of animations
        '''
        '''
        Метод инициализации сборника анимаций
        :param ms_surf: поверхность, на которой будет отрисована анимация
        :param obj: объект, за котором будет вестись наблюдение
        :param anims: {obj.state.name : list()} - словарь анимаций
        '''

        self.anims = anims
        self.obj = obj
        self.ms_surf = ms_surf

    def draw(self):
        '''
        Method that draws the animation
        '''
        '''
        Метод, отрисовывающий анимацию
        '''

        curr_anim = self.anims[self.obj.state.name]

        curr_time = self.obj.state.time
        max_time = self.obj.state.max_time
        curr_sprite_num = int(curr_time * len(curr_anim) / max_time)
        curr_sprite_num %= len(curr_anim)

        sprite = curr_anim[curr_sprite_num]

        pos = self.obj.pos.copy()
        pos[0] -= sprite.get_rect().center[0]
        pos[1] -= sprite.get_rect().center[1]

        self.ms_surf.blit(sprite, pos)


class AnimaFactory:
    '''
    Class of anima factory
    '''
    '''
    Класс фабрики, создающий коллекции анимаций
    '''

    def __init__(self, anims):
        '''
        Init method of the factory
        :param anims: {obj.state.name : list()} - dict of animations
        '''
        '''
        Метод, инициализации фабрики
        :param anims: {obj.state.name : list()} - словарь анимаций
        '''

        self. anims = anims

    def get_anima(self, ms_surf, obj):
        '''
        Method that returns new anima
        :param ms_surf: surface to blit animation on
        :param obj: obj whose state will be tracked
        '''
        '''
        Метод, возвращающий новую коллекцию анимаций
        :param ms_surf: поверхность, на которой будет отрисована анимация
        :param obj: объект, за котором будет вестись наблюдение
        '''

        return Anima(ms_surf, obj, self.anims)


sprites_loader.load()
ANIMAS_FACTORIES = dict()
for enemy_name, enemy_sprites in sprites_loader.ENEMIES_SPRITES.items():
    new_factory = AnimaFactory(enemy_sprites)
    ANIMAS_FACTORIES.update({enemy_name: new_factory})

for tower_name, tower_sprites in sprites_loader.TOWERS_SPRITES.items():
    if type(towers.TOWER_TYPES[tower_name]) == towers.AttackTowerFactory:
        new_factory = AnimaFactory(tower_sprites)
        ANIMAS_FACTORIES.update({tower_name: new_factory})
