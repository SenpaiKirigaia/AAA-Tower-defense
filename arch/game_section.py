import arch.base_arch as base_arch
import arch.vis_arch as vis_arch


class GameSection:
    '''
    Class of the game section
    '''

    def __init__(self, ms_event_manager, ms_visual_manager, gui_cls):
        '''
        Init method of the main menu
        :param ms_event_manager: link to the master event manager
        :param ms_visual_manager: link to the master visual manager
        :param gui_cls: class of the GUI to be used
        '''
        '''
        Метод инициализации главного меню
        :param ms_event_manager: ссылка на главного обработчика событий
        :param ms_visual_manager: ссылка на главный холст
        :param gui_cls: класс для создания ГПИ
        '''

        self.ms_event_manager = ms_event_manager
        self.ms_visual_manager = ms_visual_manager

        self.event_manager = base_arch.EventManager(ms_event_manager)
        self.canvas = vis_arch.Canvas(self.event_manager, ms_visual_manager,
                                      ms_visual_manager.size, (0, 0),
                                      (0, 0, 0))
        self.gui = gui_cls(self.event_manager, self.canvas, self)

    def plugin(self, ms_event_manager, ms_visual_manager):
        '''
        Method that connects the game section to the given
        evnt manager and visual manager
        :param ms_event_manager: event manager to connect to
        :param ms_visual_manager: visual manager to connect to
        '''
        '''
        Метод, подключающий игровую секция к данным менеджеру
        событий и холсту
        :param ms_event_manager: менеджер событий, к которому нужно
                                 подключиться
        :param ms_visual_manager: холст, к которому
                                  нужно подключиться
        '''

        add_1 = base_arch.Manager.ADD_OBJ(self.event_manager,
                                          address=ms_event_manager)

        add_2 = base_arch.Manager.ADD_OBJ(self.canvas,
                                          address=ms_visual_manager)

        add_3 = base_arch.Manager.ADD_OBJ(self.event_manager.clock,
                                          address=ms_event_manager.clock)
        ms_event_manager.post(add_1)
        ms_event_manager.post(add_2)
        ms_event_manager.post(add_3)

        self.ms_event_manager = ms_event_manager
        self.ms_visual_manager = ms_visual_manager

    def unplug(self):
        '''
        Method that disconects the game section from its
        event manager and visual manager
        '''
        '''
        Метод, отключающий данную игровую секцию от ее
        менеджера событий и холста
        '''
        ms_clock = self.ms_event_manager.clock

        rm_1 = base_arch.Manager.REMOVE_OBJ(self.canvas,
                                            address=self.ms_visual_manager)

        rm_2 = base_arch.Manager.REMOVE_OBJ(self.event_manager,
                                            address=self.ms_event_manager)

        rm_3 = base_arch.Manager.REMOVE_OBJ(self.event_manager.clock,
                                            address=ms_clock)
        self.ms_event_manager.post(rm_1)
        self.ms_event_manager.post(rm_2)
        self.ms_event_manager.post(rm_3)
