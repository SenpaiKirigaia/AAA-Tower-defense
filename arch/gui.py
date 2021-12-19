import pygame as pg
import pygame_gui as pg_gui
import arch.base_arch as base_arch
import arch.vis_arch as vis_arch


class GUI(base_arch.EventManager.Employee):
    '''
    Class of GUI
    '''
    '''
    Класс графического пользовательского интерфейса (ГПИ)
    '''

    class LinkedLabel:
        '''
        Class of linked label
        '''
        '''
        Класс связанной строки (GUI.Label)
        '''

        def __init__(self, label, text_func):
            '''
            Init method of linked label
            :param label: instance of GUI.Label whose text should be
                          updated automatically
            :param text_func: function that returns new text value
                              for the label
            '''
            '''
            Метод инициализации связанной строки
            :param label: объект типа GUI.Label, чей текст должен
                          автоматически обнавляться
            :param text_func: функция, возвращающая новое текстовое
                              значение строки
            '''
            self.label = label
            self.text_func = text_func

        def update(self):
            '''
            Method that updates label text
            '''
            '''
            Метод, обновляющй текст строки
            '''
            self.label.set_text(self.text_func())

    Button = pg_gui.elements.ui_button.UIButton
    Label = pg_gui.elements.ui_label.UILabel
    Panel = pg_gui.elements.ui_panel.UIPanel
    button_events = (
                     pg_gui.UI_BUTTON_PRESSED,
                     pg_gui.UI_BUTTON_DOUBLE_CLICKED,
                     pg_gui.UI_BUTTON_ON_HOVERED,
                     pg_gui.UI_BUTTON_ON_UNHOVERED,
                    )

    def __init__(self, event_manager, visual_manager, game_section,
                 theme_path=None):
        '''
        Init method of the GUI
        :param event_manager: event manager that will manage this
                              GUI
        :param visual_manager: visual manager that will manage this
                               GUI
        :param game_section: game section that owns this GUI
        :param theme_path: path to theme file of gui, default value
                           is None for the standard theme
        '''
        '''
        Метод иницализации ГПИ
        :param event_manager: менеджер событий, управляющий данным
                              ГПИ
        :param visual_manager: холст, на котором будет отрисован
                               данный ГПИ
        :param game_section: игровая секция, к которой относится
                             данный ГПИ
        :param theme_path: путь к фалу с темой для ГПИ,
                           дефолтное значение - None соответствует
                           стандарнтной теме
        '''

        base_arch.EventManager.Employee.__init__(self, event_manager)

        self.game_section = game_section
        self.visual_manager = visual_manager
        add_msg = vis_arch.Canvas.SET_GUI(target=self,
                                          address=self.visual_manager)
        self.event_manager.post(add_msg)

        self.clock = base_arch.Clock(self.event_manager,
                                     self.event_manager.clock)
        self.clock.play()

        if theme_path is None:
            self.ui_manager = pg_gui.UIManager(self.visual_manager.size)
        else:
            self.ui_manager = pg_gui.UIManager(self.visual_manager.size,
                                               theme_path)
        self.buttons = dict()
        self.labels = dict()
        self.panels = dict()
        self.linked_labels = dict()

        self.panel_init()
        self.button_init()
        self.label_init()

    def panel_init(self):
        '''
        Init method of all GUI panels
        '''
        '''
        Метод инициализации всех панелей ГПИ
        '''

        pass

    def button_init(self):
        '''
        init method of all GUI buttons
        '''
        '''
        метод инициализации всех кнопок ГПИ
        '''

        pass

    def label_init(self):
        '''
        init method of all GUI labels (including linked labels)
        '''
        '''
        метод инициализации все надписей ГПИ (в том числе связанных)
        '''

        pass

    def draw(self):
        '''
        Method that draws the GUI
        '''
        '''
        Метод, отрисовывающий ГПИ на холсте
        '''

        self.ui_manager.draw_ui(self.visual_manager.surf)

    def run(self):
        '''
        Method that describes GUI default behaviour
        '''
        '''
        Метод, описывающий дефолтное поведение ГПИ
        '''

        for lin_label in self.linked_labels.values():
            lin_label.update()
        self.ui_manager.update(self.clock.get_tick())

    def call(self, msg):
        '''
        Method that describes GUI reaction to msg
        :param msg: message the GUI will react to
        '''
        '''
        Метод, описывающий реакциию ГПИ на полученное
        сообщение
        :param msg: сообщение, отправленное ГПИ
        '''

        if isinstance(msg, base_arch.PyGameMsg):
            event = msg.content['event']
            self.ui_manager.process_events(event)
            if event.type == pg.USEREVENT:
                if event.user_type in GUI.button_events:
                    self.button_handling(event)

    def remove_element(self, element_name):
        '''
        Method that removes the gui element with given name
        :param element_name: name of the gui element to remove
        '''
        '''
        Метод, удаляющий элемент ГПИ с данным именнем
        :param element_name: имя элемента, который нужно удалить
        '''

        element = None
        if element_name in self.buttons:
            element = self.buttons[element_name]
            del self.buttons[element_name]

        elif element_name in self.panels:
            element = self.panels[element_name]
            del self.panels[element_name]

        elif element_name in self.labels:
            element = self.labels[element_name]
            del self.labels[element_name]

        elif element_name in self.linked_labels:
            element = self.linked_labels[element_name]
            del self.linked_labels[element_name]

        if element is not None:
            container = element.ui_container
            container.remove_element(element)
            self.ui_manager.get_sprite_group().remove_internal(element)

    def button_handling(self, event):
        '''
        Method for proccessing of button related events
        :param event: button related pygame event,
                      gui should proccess
        '''
        '''
        Метод, обрабатывающий события кнопок
        :param event: pygame event связанный с кнопками,
                      которое ГПИ должен обработать
        '''

        pass
