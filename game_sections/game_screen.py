import re
import pygame_gui as pg_gui
import pygame as pg
import arch.gui as gui
import arch.game_section as gm_sect
import arch.model_wrap as mod_wp
import game_sections.pause_menu as pause_menu
import game_sections.end_game_screen as end_game_screen


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
                         "./assets/gui/themes/game_screen_theme.json")

    def panel_init(self):
        '''
        Init method of all game screen GUI panels
        '''
        '''
        Метод инициализации всех панелей ГПИ игрового экрана
        '''

        shop_pnl = gui.GUI.Panel(
                                  relative_rect=pg.Rect(20, 220, 243, 330),
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

        health_pnl = gui.GUI.Panel(
                                  relative_rect=pg.Rect(20, 120, 243, 71),
                                  starting_layer_height=1,
                                  manager=self.ui_manager,
                                  object_id="health-pnl"
                                 )

        self.panels.update({"shop-pnl": shop_pnl})
        self.panels.update({"time-pnl": time_pnl})
        self.panels.update({"wave-pnl": wave_pnl})
        self.panels.update({"health-pnl": health_pnl})

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
                                   tool_tip_text="Click to pause",
                                   object_id="pause-btn"
                                  )

        shop_container = self.panels["shop-pnl"].get_container()

        buy_archer_btn = gui.GUI.Button(
                                        relative_rect=pg.Rect(9, 50,
                                                              104, 130),
                                        text="",
                                        manager=self.ui_manager,
                                        container=shop_container,
                                        tool_tip_text="Buy Archer tower",
                                        object_id="buy-ARCHER-btn"
                                       )

        buy_minigun_btn = gui.GUI.Button(
                                         relative_rect=pg.Rect(128, 50,
                                                               104, 130),
                                         text="",
                                         manager=self.ui_manager,
                                         container=shop_container,
                                         tool_tip_text="Buy Minigun tower",
                                         object_id="buy-MINIGUN-btn"
                                        )

        buy_tank_btn = gui.GUI.Button(
                                      relative_rect=pg.Rect(9, 190,
                                                            104, 130),
                                      text="",
                                      manager=self.ui_manager,
                                      container=shop_container,
                                      tool_tip_text="Buy Tank tower",
                                      object_id="buy-TANK-btn"
                                     )

        sell_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(128, 190, 104, 130),
                                   text="",
                                   manager=self.ui_manager,
                                   container=shop_container,
                                   tool_tip_text="Sell tower",
                                   object_id="sell-btn"
                                  )

        cancel_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(20, 575, 241, 60),
                                    text="",
                                    manager=self.ui_manager,
                                    visible=False,
                                    tool_tip_text="Click to cancel",
                                    object_id="cancel-btn"
                                   )

        self.buttons.update({"pause-btn": pause_btn})
        self.buttons.update({"buy-archer-btn": buy_archer_btn})
        self.buttons.update({"buy-minigun-btn": buy_minigun_btn})
        self.buttons.update({"buy-tank-btn": buy_tank_btn})
        self.buttons.update({"sell-btn": sell_btn})
        self.buttons.update({"cancel-btn": cancel_btn})

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
        health_container = self.panels["health-pnl"].get_container()
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

        health_lbl = gui.GUI.Label(
                                  relative_rect=pg.Rect(110, 10, 125, 50),
                                  text="",
                                  manager=self.ui_manager,
                                  container=health_container,
                                  object_id="health-lbl"
                                 )

        def decor(func):
            def core():
                curr, full = func()
                return f"{curr} / {full}"
            return core
        health_update = decor(self.game_section.get_model_base_health)
        health_linlbl = gui.GUI.LinkedLabel(health_lbl, health_update)

        self.linked_labels.update({"time-lbl": time_linlbl})
        self.linked_labels.update({"money-lbl": money_linlbl})
        self.linked_labels.update({"wave-lbl": wave_linlbl})
        self.linked_labels.update({"health-lbl": health_linlbl})

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

            elif re.search(r"shop-pnl\.#panel_container\..*-btn",
                           event.ui_object_id):
                self.shop_btn_handle(event)

            elif event.ui_object_id == "buy-plc-btn":
                self.buy_plc_btn_handle(event)

            elif event.ui_object_id == "sell-plc-btn":
                self.sell_plc_btn_handle(event)

            elif event.ui_object_id == "cancel-btn":
                self.buttons['buy-archer-btn'].enable()
                self.buttons['buy-minigun-btn'].enable()
                self.buttons['buy-tank-btn'].enable()
                self.buttons['sell-btn'].enable()
                self.buttons["cancel-btn"].hide()
                buttons_to_del = []
                for name in self.buttons:
                    if (re.search("buy-plc-*", name) is not None
                       or re.search("sell-plc-*", name) is not None):
                        buttons_to_del.append(name)

                for name in buttons_to_del:
                    self.remove_element(name)

    def shop_btn_handle(self, event):
        if re.search(r"shop-pnl\.#panel_container\.buy-.*-btn",
                     event.ui_object_id):

            tower_type = re.search(r"shop-pnl\.#panel_container\."
                                   r"buy-(.*)-btn",
                                   event.ui_object_id).group(1)
            model_wrap = self.game_section.model_wrap
            free_space = model_wrap.get_free_space(tower_type)

            if len(free_space) > 0:
                self.buttons['buy-archer-btn'].disable()
                self.buttons['buy-minigun-btn'].disable()
                self.buttons['buy-tank-btn'].disable()
                self.buttons['sell-btn'].disable()
                self.buttons["cancel-btn"].show()

            for i in range(len(free_space)):
                button_rect = pg.Rect(0, 0, 70, 70)
                button_rect.center = free_space[i]
                plc_btn = gui.GUI.Button(
                                         relative_rect=button_rect,
                                         text="",
                                         manager=self.ui_manager,
                                         tool_tip_text="Click to confirm",
                                         object_id="buy-plc-btn"
                                        )
                self.buttons.update({f"buy-plc-{i}": plc_btn})

        elif event.ui_object_id == "shop-pnl.#panel_container.sell-btn":
            model_wrap = self.game_section.model_wrap
            occupied_space = model_wrap.get_occupied_space()

            if len(occupied_space) > 0:
                self.buttons['buy-archer-btn'].disable()
                self.buttons['buy-minigun-btn'].disable()
                self.buttons['buy-tank-btn'].disable()
                self.buttons['sell-btn'].disable()
                self.buttons["cancel-btn"].show()

            for i in range(len(occupied_space)):
                button_rect = pg.Rect(0, 0, 70, 70)
                button_rect.center = occupied_space[i]
                plc_btn = gui.GUI.Button(
                                         relative_rect=button_rect,
                                         text="",
                                         manager=self.ui_manager,
                                         tool_tip_text="Click to confirm",
                                         object_id="sell-plc-btn"
                                        )
                self.buttons.update({f"sell-plc-{i}": plc_btn})

    def buy_plc_btn_handle(self, event):
        self.buttons['buy-archer-btn'].enable()
        self.buttons['buy-minigun-btn'].enable()
        self.buttons['buy-tank-btn'].enable()
        self.buttons['sell-btn'].enable()
        self.buttons["cancel-btn"].hide()

        model_wrap = self.game_section.model_wrap
        tower_type = model_wrap.selected_tower_type
        pos = list(event.ui_element.get_relative_rect().center)

        buy_msg = mod_wp.ModelWrap.BUY_TOWER(tower_type, pos,
                                             address=model_wrap)
        self.event_manager.post(buy_msg)

        buttons_to_del = []
        for name in self.buttons:
            if re.search("buy-plc-*", name):
                buttons_to_del.append(name)

        for name in buttons_to_del:
            self.remove_element(name)

    def sell_plc_btn_handle(self, event):
        self.buttons['buy-archer-btn'].enable()
        self.buttons['buy-minigun-btn'].enable()
        self.buttons['buy-tank-btn'].enable()
        self.buttons['sell-btn'].enable()
        self.buttons["cancel-btn"].hide()

        model_wrap = self.game_section.model_wrap
        pos = list(event.ui_element.get_relative_rect().center)

        sell_msg = mod_wp.ModelWrap.SELL_TOWER(pos,
                                               address=model_wrap)
        self.event_manager.post(sell_msg)

        buttons_to_del = []
        for name in self.buttons:
            if re.search("sell-plc-*", name):
                buttons_to_del.append(name)

        for name in buttons_to_del:
            self.remove_element(name)


class GameScreen(gm_sect.GameSection):
    '''
    Class of the game screen
    '''
    '''
    Класс меню выбора уровня
    '''

    def __init__(self, ms_event_manager, ms_visual_manager, lvl_path):
        '''
        Init method of the game screen
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        :param lvl_path: path str to the level folder
        '''
        '''
        Метод инициализации игровой экран
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
        :param lvl_path: строка с путем до папки с уровнем
         '''

        super().__init__(ms_event_manager, ms_visual_manager, GameScreenGUI)
        self.model_wrap = mod_wp.ModelWrap(self.event_manager, self.canvas,
                                           self, lvl_path)

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

    def get_model_base_health(self):
        '''
        Method that wraps the model_wrap.get_base_health()
        '''
        '''
        Метод обертка для метода model_wrap.get_base_health()
        '''

        return self.model_wrap.get_base_health()

    def end_game(self, win_flag):
        self.unplug()
        end_game_screen.EndGameScreen(self.ms_event_manager,
                                      self.ms_visual_manager,
                                      win_flag)
