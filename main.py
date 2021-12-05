import pygame as pg
import architecture as arch

FPS = 30
WIN_SIZE = (1000, 740)

pg.init()


def main():
    event_manager = arch.MasterEventManager(FPS)
    canvas = arch.MasterCanvas(event_manager, WIN_SIZE)

    while event_manager.run():
        pass

    pg.quit()


main()
