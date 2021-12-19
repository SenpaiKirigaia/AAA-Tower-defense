import pygame_gui as pg_gui
import pygame as pg
import arch.base_arch as base_arch
import arch.gui as gui
import arch.game_section as gm_sect
import game_sections.level_select as level_select


class MainMenuGUI(gui.GUI):
    '''
    Class of main menu GUI
    '''
    '''
    Класс ГПИ главного меню
    '''

    def __init__(self, event_manager, visual_manager, game_section):
        '''
        Init method of the main menu GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        '''
        '''
        Метод инициализации ГПИ главного меню
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: игровая секция, к которой относится
                             данный ГПИ
        '''

        super().__init__(event_manager, visual_manager, game_section,
                         "./assets/gui/themes/main_menu_theme.json")

    def button_init(self):
        '''
        init method of all main menu GUI buttons
        '''
        '''
        метод инициализации всех кнопок ГПИ главного меню
        '''

        start_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(350, 450, 300, 75),
                                    text="START",
                                    object_id="start-btn",
                                    manager=self.ui_manager)

        quit_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(350, 550, 300, 75),
                                   text="QUIT",
                                   object_id="quit-btn",
                                   manager=self.ui_manager)

        self.buttons.update({"start-btn": start_btn})
        self.buttons.update({"quit-btn": quit_btn})

    def label_init(self):
        '''
        init method of all GUI labels (including linked labels)
        '''
        '''
        метод инициализации все надписей ГПИ (в том числе связанных)
        '''

        title_lbl = gui.GUI.Label(
                                   relative_rect=pg.Rect(100, 200, 800, 100),
                                   text="AAA TOWER DEFENSE",
                                   manager=self.ui_manager,
                                   object_id="title")

        credits_lbl = gui.GUI.Label(
                                   relative_rect=pg.Rect(300, 250, 400, 100),
                                   text="by  SenpaiKirigaia  and  Co",
                                   manager=self.ui_manager,
                                   object_id="credits")

        self.labels.update({"credits": credits_lbl})
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
            if event.ui_object_id == "quit-btn":
                quit_msg = base_arch.MasterEventManager.QUIT()
                self.event_manager.master_manager.post(quit_msg)

            elif event.ui_object_id == 'start-btn':
                self.game_section.unplug()
                level_select.LevelSelect(self.game_section.ms_event_manager,
                                         self.game_section.ms_visual_manager)


class MainMenu(gm_sect.GameSection):
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

        super().__init__(ms_event_manager, ms_visual_manager, MainMenuGUI)
