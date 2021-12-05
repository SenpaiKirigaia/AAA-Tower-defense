import pygame_gui as pg_gui
import pygame as pg
import sys

sys.path.append("..")
import architecture as arch


class MainMenuGUI(arch.GUI):
    '''
    Class of main menu GUI
    '''
    '''
    Класс ГПИ главного меню
    '''

    def __init__(self, event_manager, visual_manager):
        '''
        Init method of the main menu GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        '''
        '''
        Метод инициализации ГПИ главного меню
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        '''

        super().__init__(event_manager, visual_manager,
                         "./arch/data/themes/main_menu_theme.json")
        self.size = visual_manager.size

        start_btn = arch.GUI.Button(
                                    relative_rect=pg.Rect(400, 500, 200, 50),
                                    text="START",
                                    manager=self.ui_manager)

        quit_btn = arch.GUI.Button(
                                   relative_rect=pg.Rect(400, 600, 200, 50),
                                   text="QUIT",
                                   manager=self.ui_manager)

        title_lbl = arch.GUI.Label(
                                   relative_rect=pg.Rect(200, 200, 600, 100),
                                   text="AAA TOWER DEFFENSE",
                                   manager=self.ui_manager,
                                   object_id="title")

        self.buttons.update({"start-btn": start_btn})
        self.buttons.update({"quit-btn": quit_btn})
        self.labels.update({"title": title_lbl})

    def button_handling(self, event):
        '''
        Method for proccessing of button related events
        :param event: button related pygame event,
                      start menu gui should proccess
        '''
        '''
        Метод, обрабатывающий события кнопок
        :param event: pygame event связанный с кнопками,
                      которое ГПИ главного меню должен обработать
        '''

        if event.user_type == pg_gui.UI_BUTTON_PRESSED:
            if event.ui_element is self.buttons['quit-btn']:
                quit_msg = arch.MasterEventManager.QUIT()
                self.event_manager.master_manager.post(quit_msg)


class MainMenu:
    '''
    Class of the main menu
    '''
    '''
    Класс главного меню
    '''

    def __init__(self, ms_event_manager, ms_visual_manager):
        '''
        Init method of the main menu
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        '''
        '''
        Метод инициализации главного меню
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
         '''

        self.event_manager = arch.EventManager(ms_event_manager)
        self.canvas = arch.Canvas(self.event_manager, ms_visual_manager,
                                  ms_visual_manager.size, (0, 0), (0, 0, 40))
        self.gui = MainMenuGUI(self.event_manager, self.canvas)
