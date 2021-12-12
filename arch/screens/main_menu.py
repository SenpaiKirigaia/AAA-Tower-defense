import pygame_gui as pg_gui
import pygame as pg
import arch.base_arch as base_arch
import arch.vis_arch as vis_arch
import arch.gui as gui
import arch.screens.level_select as level_select


class MainMenuGUI(gui.GUI):
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

        start_btn = gui.GUI.Button(
                                    relative_rect=pg.Rect(350, 450, 300, 75),
                                    text="START",
                                    manager=self.ui_manager)

        quit_btn = gui.GUI.Button(
                                   relative_rect=pg.Rect(350, 550, 300, 75),
                                   text="QUIT",
                                   manager=self.ui_manager)

        title_lbl = gui.GUI.Label(
                                   relative_rect=pg.Rect(100, 200, 800, 100),
                                   text="AAA TOWER DEFFENSE",
                                   manager=self.ui_manager,
                                   object_id="title")

        credits_lbl = gui.GUI.Label(
                                   relative_rect=pg.Rect(300, 250, 400, 100),
                                   text="by  SenpaiKirigaia  and  Co",
                                   manager=self.ui_manager,
                                   object_id="credits")

        self.buttons.update({"start-btn": start_btn})
        self.buttons.update({"quit-btn": quit_btn})
        self.labels.update({"title": title_lbl})
        self.labels.update({"credits": credits_lbl})

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
                quit_msg = base_arch.MasterEventManager.QUIT()
                self.event_manager.master_manager.post(quit_msg)

            elif event.ui_element is self.buttons['start-btn']:
                master_manager = self.event_manager.master_manager
                master_canvas = self.visual_manager.master_canvas
                master_clock = master_manager.clock

                rm_1 = base_arch.Manager.REMOVE_OBJ(self.visual_manager,
                                                    address=master_canvas)

                rm_2 = base_arch.Manager.REMOVE_OBJ(self.event_manager,
                                                    address=master_manager)

                rm_3 = base_arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                                    address=master_clock)
                level_select.LevelSelect(master_manager, master_canvas)
                master_manager.post(rm_1)
                master_manager.post(rm_2)
                master_manager.post(rm_3)


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

        self.event_manager = base_arch.EventManager(ms_event_manager)
        self.canvas = vis_arch.Canvas(self.event_manager, ms_visual_manager,
                                      ms_visual_manager.size, (0, 0),
                                      (0, 0, 0))
        self.gui = MainMenuGUI(self.event_manager, self.canvas)
