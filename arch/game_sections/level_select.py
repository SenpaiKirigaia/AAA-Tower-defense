import pygame_gui as pg_gui
import pygame as pg
import arch.gui as gui
import arch.game_section as gm_sect
import arch.game_sections.main_menu as main_menu
import arch.game_sections.game_screen as game_screen


class LevelSelectGUI(gui.GUI):
    '''
    Class of level select menu GUI
    '''
    '''
    Класс ГПИ меню выбора уровня
    '''

    def __init__(self, event_manager, visual_manager, game_section):
        '''
        Init method of the level select menu GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        '''
        '''
        Метод инициализации ГПИ меню выбора уровня
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: game section that owns this GUI
                             данный ГПИ
        '''

        super().__init__(event_manager, visual_manager, game_section,
                         "./arch/data/themes/level_select_theme.json")

    def button_init(self):
        '''
        Init method of all level select menu GUI buttons
        '''
        '''
        Метод инициализации всех кнопок ГПИ меню выбора уровня
        '''

        lvl_1_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(75, 160, 226, 218),
                                   text="",
                                   manager=self.ui_manager,
                                   object_id='lvl-1-btn')

        lvl_2_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(385, 160, 226, 218),
                                   text="",
                                   manager=self.ui_manager,
                                   object_id='lvl-2-btn')

        lvl_3_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(695, 160, 226, 218),
                                   text="",
                                   manager=self.ui_manager,
                                   object_id='lvl-3-btn')

        lvl_4_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(75, 445, 226, 218),
                                   text="",
                                   manager=self.ui_manager,
                                   object_id='lvl-4-btn')

        lvl_5_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(385, 445, 226, 218),
                                   text="",
                                   manager=self.ui_manager,
                                   object_id='lvl-5-btn')

        ret_btn = gui.GUI.Button(
                                 relative_rect=pg.Rect(695, 445, 226, 218),
                                 text="",
                                 manager=self.ui_manager,
                                 object_id='ret-btn')

        self.buttons.update({"lvl-1-btn": lvl_1_btn})
        self.buttons.update({"lvl-2-btn": lvl_2_btn})
        self.buttons.update({"lvl-3-btn": lvl_3_btn})
        self.buttons.update({"lvl-4-btn": lvl_4_btn})
        self.buttons.update({"lvl-5-btn": lvl_5_btn})
        self.buttons.update({"ret-btn": ret_btn})

    def label_init(self):
        '''
        init method of all level select menu GUI labels
        (including linked labels)
        '''
        '''
        метод инициализации все надписей ГПИ меню выбора уровная
        (в том числе связанных)
        '''

        title_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(100, 50, 800, 100),
                                  text="AAA TOWER DEFFENSE",
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
            if event.ui_object_id == "ret-btn":
                self.game_section.unplug()
                main_menu.MainMenu(self.game_section.ms_event_manager,
                                   self.game_section.ms_visual_manager)
            elif event.ui_object_id == "lvl-1-btn":
                self.game_section.unplug()
                game_screen.GameScreen(self.game_section.ms_event_manager,
                                       self.game_section.ms_visual_manager)


class LevelSelect(gm_sect.GameSection):
    '''
    Class of the level select menu
    '''
    '''
    Класс меню выбора уровня
    '''

    def __init__(self, ms_event_manager, ms_visual_manager):
        '''
        Init method of the level select menu
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        '''
        '''
        Метод инициализации меню выбора уровня
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
         '''

        super().__init__(ms_event_manager, ms_visual_manager, LevelSelectGUI)
