import pygame_gui as pg_gui
import pygame as pg
import arch.gui as gui
import arch.game_section as gm_sect
import game_sections.main_menu as main_menu


class PauseMenuGUI(gui.GUI):
    '''
    Class of pause menu GUI
    '''
    '''
    Класс ГПИ меню паузы
    '''

    def __init__(self, event_manager, visual_manager, game_section):
        '''
        Init method of the pause menu GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        '''
        '''
        Метод инициализации ГПИ меню паузы
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: игровая секция, к которой относится
                             данный ГПИ
         '''

        super().__init__(event_manager, visual_manager, game_section,
                         "./assets/gui/themes/pause_menu_theme.json")

    def button_init(self):
        '''
        init method of all pause menu GUI buttons
        '''
        '''
        метод инициализации всех кнопок ГПИ меню паузы
        '''

        main_menu_btn = gui.GUI.Button(
                                       relative_rect=pg.Rect(350, 320,
                                                             300, 90),
                                       text="MAIN MENU",
                                       object_id="main-menu-btn",
                                       manager=self.ui_manager)

        ret_btn = gui.GUI.Button(
                                 relative_rect=pg.Rect(350, 450,
                                                       300, 90),
                                 text="RETURN",
                                 object_id="ret-btn",
                                 manager=self.ui_manager)

        self.buttons.update({"main-menu-btn": main_menu_btn})
        self.buttons.update({"ret-btn": ret_btn})

    def label_init(self):
        '''
        init method of all GUI labels (including linked labels)
        '''
        '''
        метод инициализации все надписей ГПИ меню паузы (в том числе связанных)
        '''

        title_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(200, 150, 600, 100),
                                  text="PAUSE",
                                  manager=self.ui_manager,
                                  object_id="title")

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
            if event.ui_object_id == 'main-menu-btn':
                self.game_section.unplug()
                main_menu.MainMenu(self.game_section.ms_event_manager,
                                   self.game_section.ms_visual_manager)

            elif event.ui_object_id == 'ret-btn':
                ms_event_manager = self.game_section.ms_event_manager
                ms_visual_manager = self.game_section.ms_visual_manager

                self.game_section.unplug()
                self.game_section.prev_section.plugin(ms_event_manager,
                                                      ms_visual_manager)


class PauseMenu(gm_sect.GameSection):
    '''
    Class of the pause menu
    '''
    '''
    Класс меню паузы
    '''

    def __init__(self, ms_event_manager, ms_visual_manager, prev_section):
        '''
        Init method of the pause menu
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        :param prev_section: section to return to
        '''
        '''
        Метод инициализации меню паузы
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
        :param prev_section: секция, с которой была вызвана пауза
         '''

        super().__init__(ms_event_manager, ms_visual_manager, PauseMenuGUI)
        self.prev_section = prev_section
