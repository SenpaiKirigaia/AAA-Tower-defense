import pygame as pg
import numpy as np
import json
import random
import model.enemies as enemies


TOWER_SPACE = np.array((0, 255, 0))
BASE = np.array((191, 0, 255))
VOID = np.array((0, 0, 0))
PATH = np.array((255, 255, 255))


def parse_map(map_3d):
    '''
    Method that parse the array3d of the map
    and searches for possible tower places and enemy path
    :param map_3d: array3d of the map to parse
    '''
    '''
    Метод, парсящий array3d карты и ищющий возможные места для установки
    башен и путь врагов
    :param map_3d: array3d карты, которую нужно пропарсить
    '''

    tower_space = []
    anchor_points = []
    base_pos = []

    for i in range(map_3d.shape[0]):
        for j in range(map_3d.shape[1]):
            if (map_3d[i][j] == TOWER_SPACE).all():
                tower_space.append([100 * i + 50, 100 * j + 50])

            elif (map_3d[i][j] == BASE).all():
                base_pos = [100 * i + 50, 100 * j + 50]

            elif (map_3d[i][j][0] == 255 and map_3d[i][j][1] == 255
                  and not (map_3d[i][j] == PATH).all()):
                indx = map_3d[i][j][2] / 5
                anchor_points.append(([100 * i + 50, 100 * j + 50], indx))

    anchor_points.sort(key=lambda el: el[1])
    path = [point[0] for point in anchor_points]
    path.append(base_pos)

    return tower_space, path


def generate_background(map_3d):
    '''
    Method that parse the array3d of the map
    and creates level background
    :param map_3d: array3d of the map to parse
    '''
    '''
    Метод, парсящий array3d карты и создающий задний фон для уровня
    :param map_3d: array3d карты, которую нужно пропарсить
    '''

    for i in range(map_3d.shape[0]):
        for j in range(map_3d.shape[1]):
            if (map_3d[i][j] == TOWER_SPACE).all():
                map_3d[i][j] = VOID
            elif not ((map_3d[i][j] == VOID).all()
                      or (map_3d[i][j] == BASE).all()):
                map_3d[i][j] = PATH

    recolored_map = pg.surfarray.make_surface(map_3d)
    scaled_map = pg.transform.scale(recolored_map, (1000, 1000))

    return scaled_map


def load_map(file_name):
    '''
    Method that loads the map from png file,
    searches for possible tower places and enemy path
    and creates level background
    :param file_name: string with the path to the map
    '''
    '''
    Метод, загружающий карту из файла, ищющий
    возможные мета для установки башен и создающий
    путь врагов и задний фон уровня
    :param file_name: строка с путем к карте
    '''

    raw_map = pg.image.load(file_name)
    map_3d = pg.surfarray.array3d(raw_map)

    tower_space, path = parse_map(map_3d)
    background = generate_background(map_3d)
    return tower_space, path, background


def load_waves(file_name):
    '''
    Method that loads the waves of enemies from json file
    :param file_name: string with the path to the json file
    '''
    '''
    Метод, загружающий формат волн врагов из json файла
    :param file_name: строка с путем к json файлу
    '''

    file_obj = open(file_name, "r")
    raw_waves = json.load(file_obj)
    file_obj.close()
    waves = []

    for raw_wave in raw_waves:
        wave = []

        for enemy_type, number in raw_wave.items():
            for i in range(number):
                wave.append(enemies.ENEMY_TYPES[enemy_type])

        random.shuffle(wave)
        waves.append(wave)

    return waves
