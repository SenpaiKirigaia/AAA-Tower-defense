import pygame as pg
import sys
sys.path.append("./")
import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import arch.game_sections.main_menu as main_menu


FPS = 30
WIN_SIZE = (1000, 740)

pg.init()


def main():
    event_manager = base_arch.MasterEventManager(FPS)
    canvas = vis_arch.MasterCanvas(event_manager, WIN_SIZE, (0, 0, 0))
    main_menu.MainMenu(event_manager, canvas)

    while event_manager.run():
        pass

    pg.quit()


main()
