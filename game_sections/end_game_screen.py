import pygame_gui as pg_gui
import pygame as pg
import arch.gui as gui
import arch.game_section as gm_sect
import game_sections.main_menu as main_menu


class EndGameScreenGUI(gui.GUI):
    '''
    Class of end game screem GUI
    '''
    '''
    Класс ГПИ экрана оканчания игры
    '''

    def __init__(self, event_manager, visual_manager, game_section):
        '''
        Init method of the end game screen GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        '''
        '''
        Метод инициализации ГПИ экрана оканчания игры
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: игровая секция, к которой относится
                             данный ГПИ
         '''

        super().__init__(event_manager, visual_manager, game_section,
                         "./assets/gui/themes/end_game_screen_theme.json")

    def button_init(self):
        '''
        Init method of all end game screen GUI buttons
        '''
        '''
        Метод инициализации всех кнопок ГПИ экрана оканчания игры
        '''

        main_menu_btn = gui.GUI.Button(
                                       relative_rect=pg.Rect(350, 420,
                                                             300, 90),
                                       text="MAIN MENU",
                                       object_id="main-menu-btn",
                                       manager=self.ui_manager)

        self.buttons.update({"main-menu-btn": main_menu_btn})

    def label_init(self):
        '''
        Init method of all end game screen GUI labels (including linked labels)
        '''
        '''
        Метод инициализации все надписей ГПИ экрана оканчания игры
        (в том числе связанных)
        '''

        title_text = ""
        if self.game_section.win_flag:
            title_text = "YOU WON"
        else:
            title_text = "YOU LOSE"

        title_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(150, 150, 700, 100),
                                  text=title_text,
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


class EndGameScreen(gm_sect.GameSection):
    '''
    Class of the end game screen
    '''
    '''
    Класс экрана оканчания игры
    '''

    def __init__(self, ms_event_manager, ms_visual_manager, win_flag):
        '''
        Init method of the end game screen
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        '''
        '''
        Метод инициализации экрана оканчания игры
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
         '''

        self.win_flag = win_flag
        super().__init__(ms_event_manager, ms_visual_manager,
                         EndGameScreenGUI)
