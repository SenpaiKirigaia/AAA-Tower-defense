import pygame_gui as pg_gui
import pygame as pg
import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import arch.gui as gui
import arch.screens.main_menu as main_menu


class PauseMenuGUI(gui.GUI):
    '''
    Class of pause menu GUI
    '''
    '''
    Класс ГПИ меню паузы
    '''

    def __init__(self, event_manager, visual_manager, pause_screen):
        '''
        Init method of the pause menu GUI
        :param pause_screen: link to the current PauseMenuScreen
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        '''
        '''
        Метод инициализации ГПИ меню паузы
        :param pause_screen: ссылка на текущее меню паузы
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        '''

        super().__init__(event_manager, visual_manager,
                         "./arch/data/themes/pause_menu_theme.json")
        self.size = self.visual_manager.size
        self.pause_screen = pause_screen

        main_menu_btn = gui.GUI.Button(
                                        relative_rect=pg.Rect(350, 320,
                                                              300, 90),
                                        text="MAIN MENU",
                                        manager=self.ui_manager)

        ret_btn = gui.GUI.Button(
                                  relative_rect=pg.Rect(350, 450,
                                                        300, 90),
                                  text="RETURN",
                                  manager=self.ui_manager)

        title_lbl = gui.GUI.Label(
                                   relative_rect=pg.Rect(200, 150, 600, 100),
                                   text="PAUSE",
                                   manager=self.ui_manager,
                                   object_id="title")

        self.buttons.update({"main-menu-btn": main_menu_btn})
        self.buttons.update({"ret-btn": ret_btn})
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
            if event.ui_element is self.buttons['main-menu-btn']:
                master_manager = self.event_manager.master_manager
                master_canvas = self.visual_manager.master_canvas
                master_clock = master_manager.clock

                rm_1 = base_arch.Manager.REMOVE_OBJ(self.visual_manager,
                                                    address=master_canvas)

                rm_2 = base_arch.Manager.REMOVE_OBJ(self.event_manager,
                                                    address=master_manager)

                rm_3 = base_arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                                    address=master_clock)
                main_menu.MainMenu(master_manager, master_canvas)
                master_manager.post(rm_1)
                master_manager.post(rm_2)
                master_manager.post(rm_3)
            elif event.ui_element is self.buttons['ret-btn']:
                master_manager = self.event_manager.master_manager
                master_canvas = self.visual_manager.master_canvas
                master_clock = master_manager.clock

                rm_1 = base_arch.Manager.REMOVE_OBJ(self.visual_manager,
                                                    address=master_canvas)

                rm_2 = base_arch.Manager.REMOVE_OBJ(self.event_manager,
                                                    address=master_manager)

                rm_3 = base_arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                                    address=master_clock)
                master_manager.post(rm_1)
                master_manager.post(rm_2)
                master_manager.post(rm_3)

                prev_screen = self.pause_screen.prev_screen
                prev_screen_clock = prev_screen.event_manager.clock

                add_1 = base_arch.Manager.ADD_OBJ(prev_screen.canvas,
                                                  address=master_canvas)

                add_2 = base_arch.Manager.ADD_OBJ(prev_screen.event_manager,
                                                  address=master_manager)

                add_3 = base_arch.Manager.ADD_OBJ(prev_screen_clock,
                                                  address=master_clock)
                master_manager.post(add_1)
                master_manager.post(add_2)
                master_manager.post(add_3)


class PauseMenu:
    '''
    Class of the pause menu
    '''
    '''
    Класс меню паузы
    '''

    def __init__(self, ms_event_manager, ms_visual_manager, prev_screen):
        '''
        Init method of the pause menu
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        :param prev_screen: screen to return to
        '''
        '''
        Метод инициализации меню паузы
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
        :param prev_screen: экран, с которого была вызвана пауза
         '''

        self.event_manager = base_arch.EventManager(ms_event_manager)
        self.canvas = vis_arch.Canvas(self.event_manager, ms_visual_manager,
                                      ms_visual_manager.size, (0, 0),
                                      (0, 0, 0))
        self.gui = PauseMenuGUI(self.event_manager, self.canvas, self)
        self.prev_screen = prev_screen
