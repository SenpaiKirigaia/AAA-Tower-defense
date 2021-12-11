import pygame_gui as pg_gui
import pygame as pg
import sys

sys.path.append("arch")
import architecture as arch

sys.path.append("arch/screens/")
import pause_menu


class GameScreenGUI(arch.GUI):
    '''
    Class of game screen GUI
    '''
    '''
    Класс ГПИ игрового экрана
    '''

    def __init__(self, game_screen):
        '''
        Init method of the game screen GUI
        :param game_screen: link to the current game_screen
        '''
        '''
        Метод инициализации ГПИ игрового экрана
        :param game_screen: ссылка на текущий игровой экран
        '''

        super().__init__(game_screen.event_manager, game_screen.canvas,
                         "./arch/data/themes/game_screen_theme.json")
        self.size = self.visual_manager.size
        self.game_screen = game_screen
        self.panel_init()
        self.button_init()
        self.label_init()

    def panel_init(self):
        '''
        Init method of all game screen GUI panels
        '''
        '''
        Метод инициализации всех панелей ГПИ игрового экрана
        '''

        shop_pnl = arch.GUI.Panel(
                                  relative_rect=pg.Rect(20, 110, 243, 533),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="shop-pnl"
                                 )

        time_pnl = arch.GUI.Panel(
                                  relative_rect=pg.Rect(20, 20, 110, 71),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="time-pnl"
                                 )

        wave_pnl = arch.GUI.Panel(
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

        pause_btn = arch.GUI.Button(
                                    relative_rect=pg.Rect(20, 660, 241, 60),
                                    text="",
                                    manager=self.ui_manager,
                                    object_id="pause-btn"
                                   )

        shop_container = self.panels["shop-pnl"].get_container()

        buy_1_btn = arch.GUI.Button(
                                    relative_rect=pg.Rect(9, 50, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-1-btn"
                                   )

        buy_2_btn = arch.GUI.Button(
                                    relative_rect=pg.Rect(128, 50, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-2-btn"
                                   )

        buy_3_btn = arch.GUI.Button(
                                    relative_rect=pg.Rect(9, 190, 104, 130),
                                    text="",
                                    manager=self.ui_manager,
                                    container=shop_container,
                                    object_id="buy-3-btn"
                                   )

        sell_btn = arch.GUI.Button(
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

        time_lbl = arch.GUI.Label(
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
                return f"{mins:02d} : {secs:02d}"
            return core
        time_update = decor(self.event_manager.clock.get_time)
        time_linlbl = arch.GUI.LinkedLabel(time_lbl, time_update)

        money_lbl = arch.GUI.Label(
                                  relative_rect=pg.Rect(120, 15, 110, 25),
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
        money_update = decor(lambda: 0)
        money_linlbl = arch.GUI.LinkedLabel(money_lbl, money_update)

        wave_lbl = arch.GUI.Label(
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
        wave_update = decor(lambda: (0, 0))
        wave_linlbl = arch.GUI.LinkedLabel(wave_lbl, wave_update)

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
            if event.ui_element is self.buttons["pause-btn"]:
                master_manager = self.event_manager.master_manager
                master_canvas = self.visual_manager.master_canvas

                rm_1 = arch.Manager.REMOVE_OBJ(self.visual_manager,
                                               address=master_canvas)

                rm_2 = arch.Manager.REMOVE_OBJ(self.event_manager,
                                               address=master_manager)

                rm_3 = arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                               address=master_manager.clock)
                pause_menu.PauseMenu(master_manager, master_canvas,
                                     self.game_screen)
                master_manager.post(rm_1)
                master_manager.post(rm_2)
                master_manager.post(rm_3)


class GameScreen:
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

        self.event_manager = arch.EventManager(ms_event_manager)
        self.canvas = arch.Canvas(self.event_manager, ms_visual_manager,
                                  ms_visual_manager.size, (0, 0), (0, 0, 0))
        self.gui = GameScreenGUI(self)
