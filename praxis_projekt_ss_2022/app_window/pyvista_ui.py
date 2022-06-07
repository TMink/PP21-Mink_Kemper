# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import sys
import os

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QPushButton, QMainWindow, QScrollArea, QAction, QMenu, \
    QLabel, QSpacerItem, QSizePolicy, QWidget, QGridLayout, QApplication, QGroupBox, QProgressBar
from pyvistaqt import QtInteractor

from app_window.ui_elements_init import init_found_info_panel, init_interaction_objects_info_panel, \
    init_shapefile_tool_info_panel, init_menu_bar, init_key_events, init_loading_screen

from app_window.ui_elements_functions import f_checkbox_action, \
    f_checkbox_hide, f_checkbox_show, f_info_panel_hide_show, io_change_button_style, \
    io_create_not_plotted_objects_button, io_create_plotted_objects_button, io_delete_button, \
    io_info_panel_hide_show, io_object_view_mode_button, sf_info_panel_hide_show, sf_load_button, sf_checkbox_action, \
    sf_checkbox_hide, sf_checkbox_show

from app_window.ui_mesh_functions import load_interaction_mesh, load_excavation_side, load_segmentation_tool, \
    load_extraction_tool, load_shapefile_tool

from app_window.ui_outsourced_functions import build_legend, clipping, build_founds, build_dummy_object, clear_tool, \
    check_founds, callback, check_clicked_tracked, create_geotiff, update_window_height, loading_tasks_and_screen

from data.lists import *

ICON_PATH = 'resources/assets/icons8-mesh-100.png'

os.environ["QT_API"] = "pyqt5"


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Colonia MeshUp')
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setFixedSize(1100, 500)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.n = 100

        self.frame = QFrame()
        #self.myApp = Window()
        self.system_name = QLabel(self.frame)
        self.current_task = QLabel(self.frame)
        self.progressbar = QProgressBar(self.frame)
        self.loading_sign = QLabel(self.frame)
        init_loading_screen.do(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def loading(self):
        loading_tasks_and_screen.do(self, Window)


class Window(QMainWindow):
    resized = pyqtSignal()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)

        # Window size
        self.setWindowTitle('Colonia MeshUp')
        self.setWindowIcon(QIcon(ICON_PATH))
        self.setMinimumSize(1920, 1080)
        self.resized.connect(self.update_window_height)

        # whole ui layout
        self.main_layout = QHBoxLayout()

        # info panel layout
        self.info_panel_layout = QVBoxLayout()

        # create frame
        self.frame = QFrame()
        self.frame.setStyleSheet(open('resources/style_sheets/frame_style_sheet.txt').read().replace('\n', ''))
        self.frame.setLayout(self.main_layout)
        self.setCentralWidget(self.frame)

        # create plotter
        self.plotter = QtInteractor()
        self.main_layout.addWidget(self.plotter.interactor)

        self.plotter.add_background_image('resources/assets/colonia_4d_background_one_color.png')
        self.plotter.track_click_position(callback=self.check_clicked_tracked, side='l')

        # spacer item
        self.spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)



        '''
        *******************************************************************************************************
        ***                                       Found info panel                                          ***
        *******************************************************************************************************
        '''
        self.found_scroll_area_layout = QVBoxLayout()

        self.found_label = QLabel()

        self.found_scroll_area = QScrollArea()

        self.found_scroll_area_widget = QWidget()

        init_found_info_panel.do(self)



        '''
        *******************************************************************************************************
        ***                                Interaction objects info panel                                   ***
        *******************************************************************************************************
        '''
        self.interaction_objects_create_delete_button_layout = QHBoxLayout()
        self.interaction_objects_scroll_areas_layout = QHBoxLayout()
        self.interaction_accessible_objects_scroll_area_layout = QGridLayout()
        self.interaction_loaded_objects_scroll_area_layout = QGridLayout()

        self.interaction_objects_label = QLabel()

        self.scroll_interaction_objects = QScrollArea()
        self.interaction_accessible_objects_scroll_area = QScrollArea()
        self.interaction_loaded_objects_scroll_area = QScrollArea()

        self.interaction_accessible_objects_scroll_area_widget = QWidget()
        self.interaction_loaded_objects_scroll_area_widget = QWidget()

        self.interaction_objects_object_view_mode_button = QPushButton('Object/View Mode')
        self.interaction_objects_create_button = QPushButton('Create')
        self.interaction_objects_delete_button = QPushButton('Delete')

        init_interaction_objects_info_panel.do(self)



        '''
        *******************************************************************************************************
        ***                                   Shapefile Tool info panel                                     ***
        *******************************************************************************************************
        '''
        self.shapefile_tool_scroll_area_layout = QVBoxLayout()

        self.shapefile_tool_scroll_area = QScrollArea()

        self.shapefile_tool_scroll_area_widget = QWidget()

        self.shapefile_tool_load_button = QPushButton('Clip mesh')

        init_shapefile_tool_info_panel.do(self)



        '''
        *******************************************************************************************************
        ***                                      Menu Bar (main_menu)                                       ***
        *******************************************************************************************************
        ***    -> File                              (file_menu)                                             ***
        ***        -> Exit button                   (exit_button)                                           ***
        ***    -> Tools                             (tools_menu)                                            ***
        ***        -> Excavation side               (excavation_side_menu)                                  ***
        ***            -> Original textures         (excavation_side_texture)                               ***
        ***            -> Segment colors            (excavation_side_color)                                 ***
        ***        -> Segmentation Tool             (segmentation_tool_menu)                                ***
        ***            -> Original textures         (segmentation_tool_texture)                             ***
        ***            -> Segment colors            (segmentation_tool_color)                               ***
        ***        -> Extraction Tool               (extraction_tool_menu)                                  ***
        ***            -> Original textures         (extraction_tool_texture)                               ***
        ***            -> Segment colors            (extraction_tool_color)                                 ***
        ***        -> Shapefile Tool                (shapefile_tool_menu)                                   ***
        ***            -> Load Shapefiles           (shapefile_tool_load)                                   ***
        ***            -> show/hide info panel      (shapefile_tool_info_panel)                             ***
        ***    -> Interaction objects               (interaction_objects_menu)                              ***
        ***        -> show/hide object/-s           (interaction_objects_show_hide)                         ***
        ***        -> show/hide info panel          (interaction_objects_info_panel)                        ***
        ***    -> Founds                            (founds_menu)                                           ***
        ***        -> show/hide found/-s            (founds_show_hide)                                      ***
        ***        -> show/hide found info panel    (founds_info_panel)                                     ***
        *******************************************************************************************************
        '''
        self.main_menu = self.menuBar()
        self.file_menu = self.main_menu.addMenu('File')
        self.tools_menu = self.main_menu.addMenu('Tools')
        self.interaction_objects_menu = self.main_menu.addMenu('Interaction objects')
        self.founds_menu = self.main_menu.addMenu('Found/-s')
        self.geotiff_menu = self.main_menu.addMenu('GeoTiff Screenshot')

        self.excavation_side_menu = QMenu('View Excavations side', self)
        self.segmentation_tool_menu = QMenu('Segmentation Tool')
        self.extraction_tool_menu = QMenu('Extraction Tool')
        self.shapefile_menu = QMenu('Shapefile Tool')

        self.exit_button = QAction('Exit', self)
        self.excavation_side_texture = QAction('Original textures', self, checkable=True)
        self.excavation_side_color = QAction('Segment colors', self, checkable=True)
        self.segmentation_tool_texture = QAction('Original textures', self, checkable=True)
        self.segmentation_tool_color = QAction('Segment colors', self, checkable=True)
        self.extraction_tool_texture = QAction('Original textures', self, checkable=True)
        self.extraction_tool_color = QAction('Segment colors', self, checkable=True)
        self.shapefile_tool_load = QAction('Load shapefiles', self, checkable=True)
        self.geotiff_1920_1080 = QAction('1920_1080(Full HD)', self)
        self.geotiff_3840_2160 = QAction('3840_2160(4k)', self)
        self.geotiff_7680_4320 = QAction('7680_4320(8k)', self)
        self.geotiff_15360_8640 = QAction('15360_8640(16k)', self)

        self.shapefile_tool_info_panel = QAction('Info Panel', self, checkable=True)
        self.interaction_objects_info_panel = QAction('Info Panel', self, checkable=True)
        self.founds_info_panel = QAction('Info Panel', self, checkable=True)

        self.interaction_objects_show_hide = QAction('Show/Hide object/-s', self, checkable=True)
        self.founds_show_hide = QAction('Show/Hide label/-s', self, checkable=True)

        init_menu_bar.do(self)



        '''
        *******************************************************************************************************        
        ***                           Connect info_panel_layout to main_layout                              ***
        *******************************************************************************************************
        '''
        self.main_layout.addLayout(self.info_panel_layout)



        '''
        *******************************************************************************************************
        ***                                         Key events                                              ***
        *******************************************************************************************************
        '''
        init_key_events.do(self)



    '''
    ****************************************************************************************************************
    ***                                              Change view                                                 ***
    ****************************************************************************************************************
    ***                  -> top (0, 0, 1)        -> left (0, 1, 0)       -> back (1, 0, 0)                       ***
    ***                  -> bottom (0, 0, -1)    -> right (0, -1, 0)     -> front (-1, 0, 0)                     ***
    ****************************************************************************************************************
    '''
    def view_reset(self):
        self.plotter.view_isometric()

    def view_top(self):
        camera_view[0] = 'top'
        self.plotter.view_vector((0, 0, 1))
        self.plotter.camera.roll = -90

    def view_bottom(self):
        camera_view[0] = 'bottom'
        self.plotter.view_yx()
        self.plotter.camera.roll = 270.0

    def view_left(self):
        camera_view[0] = 'left'
        self.plotter.view_vector((0, -1, 0))

    def view_right(self):
        camera_view[0] = 'right'
        self.plotter.view_vector((0, 1, 0))

    def view_front(self):
        camera_view[0] = 'front'
        self.plotter.view_vector((1, 0, 0))

    def view_back(self):
        camera_view[0] = 'back'
        self.plotter.view_vector((-1, 0, 0))



    '''
    ****************************************************************************************************************
    ***                                           ui_elements_functions                                          ***
    ****************************************************************************************************************
    *** f  = founds                                                                                              ***
    *** io = interaction object                                                                                  ***
    *** st = shapefile                                                                                           ***
    ****************************************************************************************************************
    '''
    def f_checkbox_action(self, state):
        f_checkbox_action.do(self, state)

    def f_checkbox_hide(self, pos):
        f_checkbox_hide.do(pos)

    def f_checkbox_show(self, pos):
        f_checkbox_show.do(self, pos)

    def f_info_panel_hide_show(self):
        f_info_panel_hide_show.do(self)

    def io_change_button_style(self, button_name):
        io_change_button_style.do(button_name)

    def io_create_not_plotted_objects_button(self):
        io_create_not_plotted_objects_button.do(self)

    def io_create_plotted_objects_button(self):
        io_create_plotted_objects_button.do(self)

    def io_delete_button(self):
        io_delete_button.do(self)

    def io_info_panel_hide_show(self):
        io_info_panel_hide_show.do(self)

    def io_object_view_mode_button(self):
        io_object_view_mode_button.do(self)

    def sf_info_panel_hide_show(self):
        sf_info_panel_hide_show.do(self)

    def sf_load_button(self):
        sf_load_button.do(self)

    def sf_checkbox_action(self, state):
        sf_checkbox_action.do(self, state)

    def sf_checkbox_hide(self, pos):
        sf_checkbox_hide.do(pos)

    def sf_checkbox_show(self, pos):
        sf_checkbox_show.do(self, pos)

    def take_screenshot_1920_1080(self):
        create_geotiff.do(self, res=[1920, 1080])

    def take_screenshot_3840_2160(self):
        create_geotiff.do(self, res=[3840, 2160])

    def take_screenshot_7680_4320(self):
        create_geotiff.do(self, res=[7680, 4320])

    def take_screenshot_15360_8640(self):
        create_geotiff.do(self, res=[15360, 8640])



    '''
    ****************************************************************************************************************    
    ***                                             ui_mesh_functions                                            ***
    ****************************************************************************************************************
    '''
    def load_excavation_side(self, state):
        load_excavation_side.do(self, state)

    def load_extraction_tool(self, state):
        load_extraction_tool.do(self, state)

    def load_interaction_mesh(self):
        load_interaction_mesh.do(self)

    def load_segmentation_tool(self, state):
        load_segmentation_tool.do(self, state)

    def load_shapefile_tool(self, state):
        load_shapefile_tool.do(self, state)



    '''
    ****************************************************************************************************************
    ***                                        ui_outsourced_functions                                           ***
    ****************************************************************************************************************
    '''
    def build_dummy_object(self):
        build_dummy_object.do(self)

    def build_founds(self, state):
        build_founds.do(self, state)

    def build_legend(self, do):
        build_legend.do(self, do)

    def callback(self, mesh):
        callback.do(mesh)

    def check_clicked_tracked(self, click):
        check_clicked_tracked.do(self, click)

    def check_founds(self):
        check_founds.do(self)

    def clear_tool(self, use, tex_or_col):
        clear_tool.do(self, use, tex_or_col)

    def clipping(self, use, param):
        clipping.do(self, use, param)

    def create_geotiff(self, res):
        create_geotiff.do(self, res)

    def update_window_height(self):
        update_window_height.do(self)

    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)


def colonia_4d():
    app = QApplication(sys.argv)

    app.setStyleSheet('''
        #system_name {
            font-size: 80px;
            color: #DAA520;
        }
        
        #current_task {
            font-size: 30px;
            color: #BEBEBE;
        }
        
        #loading_sign {
            font-size: 30px;
            color: #BEBEBE;
        }
        
        QFrame {
            background-color: #0c1726;
            color: rgb(220, 220, 220);
        }
        
        QProgressBar {
            backgrund-color: #BEBEBE;
            color: rgb(200, 200, 200);
            border-style: none;
            border-radius: 10px;
            text-align: center;
            font-size: 30px
        }
        
        QProgressBar::chunk {
            border-radius: 10px;
            background-color: #E69F56;
        }
    ''')

    loading_screen = LoadingScreen()
    loading_screen.show()

    sys.exit(app.exec_())
