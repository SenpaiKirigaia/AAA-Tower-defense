import pygame as pg
import sys

sys.path.append("./arch/")
import architecture as arch

sys.path.append("./arch/screens/")
import main_menu


FPS = 30
WIN_SIZE = (1000, 740)

pg.init()


def main():
    event_manager = arch.MasterEventManager(FPS)
    canvas = arch.MasterCanvas(event_manager, WIN_SIZE)
    main_menu.MainMenu(event_manager, canvas)

    while event_manager.run():
        pass

    pg.quit()


main()
