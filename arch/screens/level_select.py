import pygame_gui as pg_gui
import pygame as pg
import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import arch.gui as gui
import arch.screens.main_menu as main_menu
import arch.screens.game_screen as game_screen


class LevelSelectGUI(gui.GUI):
    '''
    Class of level select menu GUI
    '''
    '''
    Класс ГПИ меню выбора уровня
    '''

    def __init__(self, event_manager, visual_manager):
        '''
        Init method of the level select menu GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        '''
        '''
        Метод инициализации ГПИ меню выбора уровня
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        '''

        super().__init__(event_manager, visual_manager,
                         "./arch/data/themes/level_select_theme.json")
        self.size = visual_manager.size

        title_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(100, 50, 800, 100),
                                  text="AAA TOWER DEFFENSE",
                                  manager=self.ui_manager,
                                  object_id="title")

        self.labels.update({"title": title_lbl})
        self.button_init()

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
            if event.ui_element is self.buttons["ret-btn"]:
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

            elif event.ui_element is self.buttons["lvl-1-btn"]:
                master_manager = self.event_manager.master_manager
                master_canvas = self.visual_manager.master_canvas
                master_clock = master_manager.clock

                rm_1 = base_arch.Manager.REMOVE_OBJ(self.visual_manager,
                                                    address=master_canvas)

                rm_2 = base_arch.Manager.REMOVE_OBJ(self.event_manager,
                                                    address=master_manager)

                rm_3 = base_arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                                    address=master_clock)
                game_screen.GameScreen(master_manager, master_canvas)
                master_manager.post(rm_1)
                master_manager.post(rm_2)
                master_manager.post(rm_3)


class LevelSelect:
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

        self.event_manager = base_arch.EventManager(ms_event_manager)
        self.canvas = vis_arch.Canvas(self.event_manager, ms_visual_manager,
                                      ms_visual_manager.size, (0, 0),
                                      (0, 0, 0))
        self.gui = LevelSelectGUI(self.event_manager, self.canvas)
