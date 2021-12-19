import pygame as pg
import pathlib
import model.enemies
import model.towers


ENEMIES_SPRITES = dict()
TOWERS_SPRITES = dict()


def load_img_dir(path_str):
    '''
    Method that loads all the imgs from the directory
    :param path_str: string with path to directory
    '''
    '''
    Метод, загружающий все изображения из директории
    :param path_str: строка с путем к директории
    '''

    imgs = []
    path = pathlib.Path(path_str)
    for img_name in path.iterdir():
        imgs.append((pg.image.load(img_name), int(img_name.stem)))
    imgs.sort(key=lambda el: el[1])
    imgs = [el[0] for el in imgs]
    return imgs


def load():
    '''
    Method that loads sprites of towers and enemies
    '''
    '''
    Метод, загружащий спрайты башен и врагов
    '''

    for enemy_type in model.enemies.ENEMY_TYPES:
        path_str = f"assets/sprites/enemies/{enemy_type.lower()}/"
        enemy_dir = pathlib.Path(path_str)
        animas = dict()
        for anima_dir in enemy_dir.iterdir():
            imgs = load_img_dir(anima_dir.as_posix())
            animas.update({f"{anima_dir.stem}": imgs})
        ENEMIES_SPRITES.update({enemy_type: animas})

    for tower_type in model.towers.TOWER_TYPES:
        path_str = f"assets/sprites/towers/{tower_type.lower()}/"
        tower_dir = pathlib.Path(path_str)
        animas = dict()
        for anima_dir in tower_dir.iterdir():
            imgs = load_img_dir(anima_dir.as_posix())
            animas.update({f"{anima_dir.stem}": imgs})
        TOWERS_SPRITES.update({tower_type: animas})
