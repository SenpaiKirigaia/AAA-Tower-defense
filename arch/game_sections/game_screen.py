import pygame_gui as pg_gui
import pygame as pg
import arch.gui as gui
import arch.game_section as gm_sect
import arch.model_wrap as mod_wp
import arch.game_sections.pause_menu as pause_menu


class GameScreenGUI(gui.GUI):
    '''
    Class of game screen GUI
    '''
    '''
    Класс ГПИ игрового экрана
    '''

    def __init__(self, event_manager, visual_manager, game_section):
        '''
        Init method of the game screen GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        '''
        '''
        Метод инициализации ГПИ игрового экрана
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: игровая секция, к которой относится
                             данный ГПИ
         '''

        super().__init__(event_manager, visual_manager, game_section,
                         "./arch/data/themes/game_screen_theme.json")

    def panel_init(self):
        '''
        Init method of all game screen GUI panels
        '''
        '''
        Метод инициализации всех панелей ГПИ игрового экрана
        '''

        shop_pnl = gui.GUI.Panel(
                                  relative_rect=pg.Rect(20, 110, 243, 533),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="shop-pnl"
                                 )

        time_pnl = gui.GUI.Panel(
                                  relative_rect=pg.Rect(20, 20, 110, 71),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="time-pnl"
                                 )

        wave_pnl = gui.GUI.Panel(
                                  relative_rect=pg.Rect(150, 20, 110, 71),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="wave-pnl"
                                 )

        self.panels.update({"shop-pnl": shop_pnl})
        self.panels.update({"time-pnl": time_pnl})
        self.panels.update({"wave-pnl": wave_pnl})

    def button_init(self):
        '''
        Init method of all game screen GUI buttons
        '''
        '''
        Метод инициализации всех кнопок ГПИ игрового экрана
        '''

        pause_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(20, 660, 241, 60),
                                    text="",
                                    manager=self.ui_manager,
                                    object_id="pause-btn"
                                   )

        shop_container = self.panels["shop-pnl"].get_container()

        buy_1_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(9, 50, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-1-btn"
                                   )

        buy_2_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(128, 50, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-2-btn"
                                   )

        buy_3_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(9, 190, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-3-btn"
                                   )

        sell_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(128, 190, 104, 130),
                                   text="",
                                   manager=self.ui_manager,
                                   container=shop_container,
                                   object_id="sell-btn"
                                  )

        self.buttons.update({"pause-btn": pause_btn})
        self.buttons.update({"buy-1-btn": buy_1_btn})
        self.buttons.update({"buy-2-btn": buy_2_btn})
        self.buttons.update({"buy-3-btn": buy_3_btn})
        self.buttons.update({"sell-btn": sell_btn})

    def label_init(self):
        '''
        Init method of all game screen GUI labels (including linked labels)
        '''
        '''
        Метод инициализации все надписей ГПИ игрового экрана
        (в том числе связанных)
        '''

        time_container = self.panels["time-pnl"].get_container()
        wave_container = self.panels["wave-pnl"].get_container()
        shop_container = self.panels["shop-pnl"].get_container()

        time_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(10, 40, 90, 25),
                                  text="",
                                  manager=self.ui_manager,
                                  container=time_container,
                                  object_id="time-lbl"
                                 )

        def decor(func):
            def core():
                time = int(func())
                secs = time % 60
                mins = time // 60
                return f"{mins:02d}:{secs:02d}"
            return core
        time_update = decor(self.game_section.get_model_time)
        time_linlbl = gui.GUI.LinkedLabel(time_lbl, time_update)

        money_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(127, 18, 110, 25),
                                  text="",
                                  manager=self.ui_manager,
                                  container=shop_container,
                                  object_id="money-lbl"
                                 )

        def decor(func):
            def core():
                money = func()
                return f"{money:05d}"
            return core
        money_update = decor(self.game_section.get_model_money)
        money_linlbl = gui.GUI.LinkedLabel(money_lbl, money_update)

        wave_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(10, 40, 90, 25),
                                  text="",
                                  manager=self.ui_manager,
                                  container=wave_container,
                                  object_id="wave-lbl"
                                 )

        def decor(func):
            def core():
                curr, full = func()
                return f"{curr}/{full}"
            return core
        wave_update = decor(self.game_section.get_model_wave)
        wave_linlbl = gui.GUI.LinkedLabel(wave_lbl, wave_update)

        self.linked_labels.update({"time-lbl": time_linlbl})
        self.linked_labels.update({"money-lbl": money_linlbl})
        self.linked_labels.update({"wave-lbl": wave_linlbl})

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
            if event.ui_object_id == "pause-btn":
                self.game_section.unplug()
                pause_menu.PauseMenu(self.game_section.ms_event_manager,
                                     self.game_section.ms_visual_manager,
                                     self.game_section)


class GameScreen(gm_sect.GameSection):
    '''
    Class of the game screen
    '''
    '''
    Класс меню выбора уровня
    '''

    def __init__(self, ms_event_manager, ms_visual_manager):
        '''
        Init method of the game screen
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        '''
        '''
        Метод инициализации игровой экран
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
         '''

        super().__init__(ms_event_manager, ms_visual_manager, GameScreenGUI)
        self.model_wrap = mod_wp.ModelWrap(self.event_manager, self.canvas)

    def get_model_time(self):
        '''
        Method that wraps the model_wrap.clock.get_time()
        '''
        '''
        Метод обертка для метода model_wrap.clock.get_time()
        '''

        return self.model_wrap.clock.get_time()

    def get_model_money(self):
        '''
        Method that wraps the model_wrap.get_money()
        '''
        '''
        Метод обертка для метода model_wrap.get_money()
        '''

        return self.model_wrap.get_money()

    def get_model_wave(self):
        '''
        Method that wraps the model_wrap.get_wave()
        '''
        '''
        Метод обертка для метода model_wrap.get_wave()
        '''

        return self.model_wrap.get_wave()
