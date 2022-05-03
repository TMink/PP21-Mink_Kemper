# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QScrollArea, QMenu, \
    QPushButton, QSpacerItem, QSizePolicy
from pyvistaqt import QtInteractor
from data.dictionarys import *
from data.lists import *
from app_functions.general_data_manipulation import change_label_color

os.environ["QT_API"] = "pyqt5"


# Ui setup
class UiMainWindow(object):
    def setup_ui(self, main_window):
        main_window.setObjectName('MainWindow')
        main_window.setWindowTitle('MainWindow')
        main_window.resize(1500, 900)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName('centralWidnget')
        main_window.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(main_window)


class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        ui = UiMainWindow()
        ui.setup_ui(self)
        self.setMinimumSize(1500, 900)
        self.resized.connect(self.update_height)

        # create the frame
        self.frame = QFrame()
        self.frame.setStyleSheet(open('resources/style_sheets/frame_style_sheet.txt').read().replace('\n', ''))

        # whole body
        vlayout = QHBoxLayout()

        # right side panel
        panels = QVBoxLayout()

        # pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)

        self.plotter.add_background_image('resources/assets/colonia_4d_background_one_color.png')

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        '''
        ***************************************
        *** Labels info panel (ui settings) ***
        ***************************************
        '''
        # Label
        self.labels_info_panel = QLabel()
        self.labels_info_panel.setStyleSheet(
            open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
        self.labels_info_panel.setFont(QFont('helvetiker regular', 15))
        self.labels_info_panel.setText('Hello World')
        self.labels_info_panel.setAutoFillBackground(True)
        self.labels_info_panel.setFixedWidth(500)
        self.labels_info_panel.hide()
        panels.addWidget(self.labels_info_panel, alignment=QtCore.Qt.AlignTop)

        # checkbox

        for i in range(0, len(label_coordinates)):
            checkbox = QCheckBox(label_names[i])
            checkbox.setObjectName(f'checkbox_{i}')
            check_boxes[f'checkbox_{i}'] = checkbox
            labels_checkboxes[f'checkbox_{i}'] = label_names[i]

        for elem in check_boxes.values():
            elem.setStyleSheet(open('resources/style_sheets/checkbox_style_sheet.txt').read().replace('\n', ''))
            elem.setFont(QFont('helvetiker regular', 10))
            elem.setFixedWidth(440)
            elem.stateChanged.connect(self.check_box_action)

        # scroll area
        self.scroll_labels = QScrollArea()
        self.scroll_labels.setWidgetResizable(True)
        self.scroll_labels.setStyleSheet('background-color: white;')
        self.scroll_labels.verticalScrollBar().setStyleSheet(
            open('resources/style_sheets/vertical_scroll_bar_style_sheet.txt').read().replace('\n', ''))
        self.scroll_labels.setFixedWidth(500)
        self.scroll_labels_Content = QWidget()
        self.scroll_labels_Layout = QVBoxLayout(self.scroll_labels_Content)
        self.scroll_labels_Content.setLayout(self.scroll_labels_Layout)
        for elem in check_boxes.values():
            self.scroll_labels_Layout.addWidget(elem)
        self.spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_labels_Layout.addItem(self.spacer_item)
        self.scroll_labels.setWidget(self.scroll_labels_Content)
        self.scroll_labels.hide()
        panels.addWidget(self.scroll_labels)

        '''
        ****************************************
        *** Objects info panel (ui settings) ***
        ****************************************
        '''
        # Label
        self.objects_info_panel = QLabel()
        self.objects_info_panel.setStyleSheet(
            open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
        self.objects_info_panel.setFont(QFont('helvetiker regular', 15))
        self.objects_info_panel.setText('Hello World')
        self.objects_info_panel.setAutoFillBackground(True)
        self.objects_info_panel.setFixedWidth(500)
        self.objects_info_panel.hide()
        panels.addWidget(self.objects_info_panel, alignment=QtCore.Qt.AlignTop)

        '''
        ****************************************
        *** Interaction object (ui settings) ***
        ****************************************
        '''
        self.button = QPushButton()
        self.button.setText('Add interactable object')
        self.button.setFixedWidth(500)
        self.button.setStyleSheet('background-color: #DAA520;')

        self.scroll_interactable_objects = QScrollArea()
        self.scroll_interactable_objects.setFixedWidth(500)
        self.scroll_interactable_objects.setStyleSheet('background-color: white;')
        self.scroll_interactable_objects_Content = QWidget(self.scroll_interactable_objects)
        self.scroll_interactable_objects_Layout = QVBoxLayout(self.scroll_interactable_objects_Content)
        self.scroll_interactable_objects_Content.setLayout(self.scroll_interactable_objects_Layout)
        self.scroll_interactable_objects_Layout.addWidget(self.button)
        self.scroll_interactable_objects.hide()
        panels.addWidget(self.scroll_interactable_objects)

        vlayout.addLayout(panels)

        '''
        ****************
        *** Menu Bar ***
        ****************
            -> File
                -> Exit button
            -> Tools
                -> Excavation side
                -> Segmentation Tool
                    -> Original textures
                    -> Segment colors
                -> Extraction Tool
                    -> Original textures
                    -> Segment colors
                -> Shapefile Tool
                    -> Original textures
                    -> Segment colors
                    -> show/hide info panel
            -> Interactable Objects
                -> show/hide object/-s
                -> show/hide info panel
            -> Labels
                -> show/hide label/-s
                -> show/hide label info panel
        '''
        # *** Menu Bar ***
        main_menu = self.menuBar()
        main_menu.setStyleSheet(open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))
        main_menu.setMinimumHeight(40)
        main_menu.setFont(QFont('helvetiker regular', 13))

        # ** File **
        file_menu = main_menu.addMenu('File')
        file_menu.setFont(QFont('helvetiker regular', 10))

        # * Exit button *
        self.exit_button = QAction('Exit', self)
        self.exit_button.setShortcut('Ctrl+Q')
        self.exit_button.triggered.connect(self.close)
        file_menu.addAction(self.exit_button)

        # ** Tools **
        tools_menu = main_menu.addMenu('Tools')
        tools_menu.setFont(QFont('helvetiker regular', 10))

        # * Excavation side *
        self.excavation_side = QAction('View Excavations side', self)
        self.excavation_side.triggered.connect(self.load_excavation_side)
        tools_menu.addAction(self.excavation_side)

        # * Segmentation tool *
        self.segmentation_menu = QMenu('Segmentation Tool')
        self.segmentation_menu.setStyleSheet(
            open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

        self.segmentation_tool_textures = QAction('Original textures', self, checkable=True)
        self.segmentation_tool_textures.setStatusTip('With textures')
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_textures.triggered.connect(self.load_segmentation_tool)

        self.segmentation_tool_color = QAction('Segment colors', self, checkable=True)
        self.segmentation_tool_color.setStatusTip('With color')
        self.segmentation_tool_color.setChecked(False)
        self.segmentation_tool_color.triggered.connect(self.load_segmentation_tool)

        self.segmentation_menu.addAction(self.segmentation_tool_textures)
        self.segmentation_menu.addAction(self.segmentation_tool_color)
        tools_menu.addMenu(self.segmentation_menu)

        # * Extraction tool *
        self.extraction_menu = QMenu('Extraction Tool')
        self.extraction_menu.setStyleSheet(
            open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

        self.extraction_tool_textures = QAction('Original textures', self, checkable=True)
        self.extraction_tool_textures.setStatusTip('With textures')
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_textures.triggered.connect(self.load_extraction_tool)

        self.extraction_tool_color = QAction('Segment colors', self, checkable=True)
        self.extraction_tool_color.setStatusTip('With color')
        self.extraction_tool_color.setChecked(False)
        self.extraction_tool_color.triggered.connect(self.load_extraction_tool)

        self.extraction_menu.addAction(self.extraction_tool_textures)
        self.extraction_menu.addAction(self.extraction_tool_color)
        tools_menu.addMenu(self.extraction_menu)

        # * Shapefile tool *
        self.shapefile_menu = QMenu('Shapefile Tool')
        self.shapefile_menu.setStyleSheet(
            open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

        self.shapefile_tool_textures = QAction('Original textures', self, checkable=True)
        self.shapefile_tool_textures.setStatusTip('With textures')
        self.shapefile_tool_textures.setChecked(False)
        self.shapefile_tool_textures.triggered.connect(self.load_shapefile_tool)

        self.shapefile_tool_color = QAction('Segment colors', self, checkable=True)
        self.shapefile_tool_color.setStatusTip('With color')
        self.shapefile_tool_color.setChecked(False)
        self.shapefile_tool_color.triggered.connect(self.load_shapefile_tool)

        self.shapefile_menu.addAction(self.shapefile_tool_textures)
        self.shapefile_menu.addAction(self.shapefile_tool_color)
        tools_menu.addMenu(self.shapefile_menu)

        # ** Interactable Object/-s **
        objects_menu = main_menu.addMenu('Objects')
        objects_menu.setFont(QFont('helvetiker regular', 10))

        # * show/hide object/-s *
        self.objects = QAction('Show/Hide object/-s', self, checkable=True)
        self.objects.setStatusTip('Load Labels')
        self.objects.setChecked(False)
        # self.objects.triggered.connect(# TODO: add function name)
        objects_menu.addAction(self.objects)

        # * Info panel *
        self.objects_panel = QAction('Info Panel', self, checkable=True)
        self.objects_panel.setStatusTip('Show/Hide label info panel')
        self.objects_panel.setChecked(False)
        self.objects_panel.triggered.connect(self.hide_show_objects_side_panel)
        objects_menu.addAction(self.objects_panel)

        # ** Labels **
        label_menu = main_menu.addMenu('Label/-s')
        label_menu.setFont(QFont('helvetiker regular', 10))

        # * shows/hide labels *
        self.labels = QAction('Show/Hide label/-s', self, checkable=True)
        self.labels.setStatusTip('Load Labels')
        self.labels.setChecked(False)
        self.labels.triggered.connect(self.load_labels)
        label_menu.addAction(self.labels)

        # * Info panel *
        self.labels_panel = QAction('Info Panel', self, checkable=True)
        self.labels_panel.setStatusTip('Show/Hide label info panel')
        self.labels_panel.setChecked(False)
        self.labels_panel.triggered.connect(self.hide_show_label_info_panel)
        label_menu.addAction(self.labels_panel)

        '''
        ******************
        *** Key events ***
        ******************
        '''
        self.plotter.add_key_event('F1', self.view_reset)
        self.plotter.add_key_event('F2', self.view_top)
        self.plotter.add_key_event('F3', self.view_bottom)
        self.plotter.add_key_event('F4', self.view_left)
        self.plotter.add_key_event('F5', self.view_right)
        self.plotter.add_key_event('F6', self.view_back)
        self.plotter.add_key_event('F7', self.view_front)

        self.plotter.add_key_event('l', self.example_surface_cut)

        self.plotter.add_key_event('j', self.interaction_mode)

    '''
    *******************
    *** Change view ***
    *******************
    Changes the view in relation so a certain vector
        -> top (0, 0, 1)
        -> bottom (0, 0, -1)
        -> left (0, 1, 0)
        -> right (0, -1, 0)
        -> back (1, 0, 0)
        -> front (-1, 0, 0)
    '''

    def view_reset(self):
        self.plotter.view_isometric()

    def view_top(self):
        self.plotter.view_vector((0, 0, 1))
        self.plotter.camera.roll = 180.0

    def view_bottom(self):
        self.plotter.view_vector((0, 0, -1))
        self.plotter.camera.roll = 360.0

    def view_left(self):
        self.plotter.view_vector((0, 1, 0))

    def view_right(self):
        self.plotter.view_vector((0, -1, 0))

    def view_back(self):
        self.plotter.view_vector((1, 0, 0))

    def view_front(self):
        self.plotter.view_vector((-1, 0, 0))

    '''
    ********************
    *** UI functions ***
    ********************
    '''

    def example_surface_cut(self):
        self.clear_tool(use='excavation_tool')

        #arc = pv.CircularArc([0, -4, -1], [0, 4, -1], [0, 0, -1])
        #arc = arc.extrude([0, 0, 2], inplace=True)
        #arc = arc.rotate_z(180)
        #poly_arc = pv.PolyData(arc)
        tube = pv.Tube()
        tube = tube.rotate_y(90)
        tube = tube.translate((0, 0, -0.5))

        label = [tube.center[0] + 1, tube.center[1], tube.center[2]]
        poly_label = pv.PolyData(label)
        visible_labels = {}

        # mesh = decimated_meshes[0]
        #mesh = next(iter(decimated_meshes.items()))[1]
        #mesh2 = list(decimated_meshes.items())[1][1]
        #print(mesh.volume - mesh.volume)
        #label = [mesh.center[0] + 3, mesh.center[1] + 3, mesh.center[2]]
        #poly_label = pv.PolyData(label)

        #clip = mesh.clip_surface(tube, invert=True)
        #clip3 = mesh2.clip_surface(tube, invert=True)
        #clip2 = poly_label.clip_surface(poly_arc)
        #if clip2.number_of_points > 0:
        #    self.plotter.add_point_labels(points=poly_label.points, labels=['item_label'], point_size=20,
        #                                  font_size=36, name='label_12', reset_camera=False)
        #self.plotter.add_mesh(tube, style='wireframe', show_scalar_bar=False)
        #self.plotter.add_mesh(clip, color='green')
        #self.plotter.add_mesh(clip3, color='blue')

        tube_holes = tube.fill_holes(1000)

        #shapefile = shapefiles[0]
        #shapefile_holes = shapefile.fill_holes(100000000000000000000000000000)


        select = poly_label.select_enclosed_points(tube_holes)
        points_inside_box = select['SelectedPoints']

        for selected, point in zip(points_inside_box, label):
            if selected == 1:
                visible_labels['label'] = point

        if 1 in points_inside_box:
            for idx, key in enumerate(visible_labels):
                name = 'label_{}'.format(idx)
                labels[name] = self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key],
                                                             point_size=20, font_size=36, name=name,
                                                             reset_camera=False)

        #self.plotter.add_mesh(tube, color='red')
        #self.plotter.add_mesh(tube_edges, color='green')
        #self.plotter.add_mesh(tube_delunay, color='blue')
        self.plotter.add_mesh(tube_holes, color='blue')

    # shows the element and adds a new spacer_item
    def show_checkbox(self, pos):
        self.scroll_labels_Layout.removeItem(self.spacer_item)
        for elem in check_boxes.values():
            if elem.objectName() == 'checkbox_%d' % pos:
                elem.show()
        self.scroll_labels_Layout.addItem(self.spacer_item)

    # hides a checkbox
    def hide_checkbox(self, pos):
        for elem in check_boxes.values():
            if elem.objectName() == 'checkbox_%d' % pos:
                elem.hide()

    # emits a signal is window is manually resized
    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    # updates the height of the info panel in comparison to the actual window height
    def update_height(self):
        self.labels_info_panel.setFixedHeight(self.height() / 2)
        self.objects_info_panel.setFixedHeight(self.height() / 2)

    # check box in side panel
    def check_box_action(self, state):
        if QtCore.Qt.Checked == state:
            change_label_color()
            self.check_labels(colored=colored_labels)
            self.interaction_mode()
            self.labels_info_panel.setText('Interactionmode On')
        else:
            change_label_color()
            self.check_labels(colored=colored_labels)
            self.interaction_mode()
            self.labels_info_panel.setText('Interactionmode Off')

    # hides/shows the labels info panel
    def hide_show_label_info_panel(self):
        if self.labels_info_panel.isHidden() and self.scroll_labels.isHidden():
            self.objects_info_panel.hide()
            self.objects_panel.setChecked(False)
            self.labels_info_panel.show()
            self.scroll_labels.show()
            self.labels_panel.setChecked(True)
        else:
            self.labels_info_panel.hide()
            self.scroll_labels.hide()
            self.labels_panel.setChecked(False)

    # hides/shows the objects info panel
    def hide_show_objects_side_panel(self):
        if self.objects_info_panel.isHidden():
            self.labels_info_panel.hide()
            self.scroll_labels.hide()
            self.labels_panel.setChecked(False)
            self.objects_info_panel.show()
            self.objects_panel.setChecked(True)
        else:
            self.objects_info_panel.hide()
            self.objects_panel.setChecked(False)

    '''
    *************************
    *** Interaction Style ***
    *************************
    '''

    # makes interaction with every actor possible
    def interaction_mode(self):
        if interaction_style[0] == 0 and interaction_actors:
            self.plotter.enable_trackball_actor_style()
            self.plotter.pickable_actors = plotted_interaction_actors
            interaction_style[0] = 1
        elif interaction_style[0] == 1 and interaction_actors:
            self.plotter.enable_trackball_style()
            self.plotter.pickable_actors = excavation_layers.values()
            interaction_style[0] = 0

    '''
    **************************************
    *** Loading/Manipulation of meshes ***
    **************************************
    '''

    # custom object
    def load_interaction_mesh(self):
        if excavation_layers or clipped_layers_seg_ex:
            interaction_actors.clear()
            plotted_interaction_actors.clear()
            # self.hide_show_interaction_side_panel()
            mesh = pv.Cube()
            name = 'Cube'
            mesh.translate(next(iter(decimated_meshes.items()))[1].center, inplace=True)
            plotted_interaction_actors.append(self.plotter.add_mesh(mesh=mesh, name=name))
            interaction_actors.append(name)

    # excavation side segments
    def load_excavation_side(self):
        # In case the user switches between tools and do not uncheck them, the semaphore get reset
        dummy_semaphore[0] = 1

        # clear and reset
        self.plotter.remove_actor(excavation_layers.keys())
        self.plotter.remove_actor(clipped_layers_seg_ex.keys())
        self.plotter.clear_plane_widgets()
        self.plotter.clear_box_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        excavation_layers.clear()
        clipped_layers_seg_ex.clear()

        if self.labels.isChecked():
            self.check_labels()

        if decimated_meshes:
            for idx, (mesh_name, mesh_data, color) in enumerate(
                    zip(decimated_meshes.keys(), decimated_meshes.values(), colors)):
                excavation_layers[mesh_name] = self.plotter.add_mesh(mesh=mesh_data, name=mesh_name, color=color,
                                                                     label=mesh_name)

        self.plotter.add_legend(bcolor='#0c1726', face="r", loc="upper left", size=(0.1, 0.1))

    # all given labels
    def load_labels(self, state):
        if state:
            if excavation_layers or clipped_layers_seg_ex or clipped_layers_shp:
                self.check_labels()
        else:
            self.plotter.remove_actor(labels.keys())

    # segmentation tool
    def load_segmentation_tool(self, state):

        # clear and reset
        self.plotter.clear_box_widgets()
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        self.plotter.remove_actor(labels.keys())
        if dummy_semaphore[0] == 1:
            self.load_dummy_object()
            dummy_semaphore[0] = 0

        def clip_mesh(normal, origin):
            extraction_semaphor[0] = 2
            self.clipping(use='segmentation', param=[normal, origin])

        if state:
            if self.segmentation_tool_textures.isChecked() and segmentation_semaphor[0] != 0:
                segmentation_semaphor[0] = 0
                self.clear_tool(use='segmentation_tool', tex_or_col='tex')
            elif self.segmentation_tool_color.isChecked() and segmentation_semaphor[0] != 1:
                segmentation_semaphor[0] = 1
                self.clear_tool(use='segmentation_tool', tex_or_col='col')
            self.plotter.add_plane_widget(clip_mesh, normal_rotation=False)
        else:
            if self.labels.isChecked():
                self.check_labels()
            dummy_semaphore[0] = 1
            self.plotter.clear_plane_widgets()

    # extraction tool
    def load_extraction_tool(self, state):
        # clear and reset
        self.plotter.clear_plane_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.plotter.remove_actor(labels.keys())
        if dummy_semaphore[0] == 1:
            self.load_dummy_object()
            dummy_semaphore[0] = 0

        def clip_mesh(box):
            segmentation_semaphor[0] = 2
            self.clipping(use='extraction', param=[box])

        if state:
            if self.extraction_tool_textures.isChecked() and extraction_semaphor[0] != 0:
                extraction_semaphor[0] = 0
                self.clear_tool(use='extraction_tool', tex_or_col='tex')
            elif self.extraction_tool_color.isChecked() and extraction_semaphor[0] != 1:
                extraction_semaphor[0] = 1
                self.clear_tool(use='extraction_tool', tex_or_col='col')
            self.plotter.add_box_widget(clip_mesh, rotation_enabled=False)
        else:
            self.check_labels()
            dummy_semaphore[0] = 1
            self.plotter.clear_box_widgets()

    def load_shapefile_tool(self):


        # clear and reset
        self.plotter.remove_actor(excavation_layers.keys())
        self.plotter.remove_actor(clipped_layers_seg_ex.keys())
        self.plotter.clear_plane_widgets()
        self.plotter.clear_box_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        excavation_layers.clear()
        clipped_layers_seg_ex.clear()

        self.shapefile_tool_textures.setChecked(True)
        self.shapefile_tool_color.setChecked(True)

        shapefile = pv.Tube(radius=2.0)
        shapefiles.append(shapefile)
        shapefile.rotate_y(90)
        shapefile.translate(next(iter(decimated_meshes.items()))[1].center)

        for key, value in decimated_meshes.items():
            clipped_layers_shp[key] = value.clip_surface(shapefile, invert=True)

        for elem in clipped_layers_shp.values():
            self.plotter.add_mesh(elem, color='green')

        shapefile = shapefile.fill_holes(100)
        self.plotter.add_mesh(shapefile, style='wireframe', color='red')

        if self.labels.isChecked():
            self.check_labels()



        #if self.labels.isChecked():
        #    self.check_labels()


        #self.clear_tool(use='excavation_tool')

        #arc = pv.CircularArc([0, -4, -1], [0, 4, -1], [0, 0, -1])
        #arc = arc.extrude([0, 0, 2], inplace=True)
        #arc = arc.rotate_z(180)
        #poly_arc = pv.PolyData(arc)
        #tube = pv.Tube()
        #tube = tube.rotate_y(90)
        #tube = tube.translate((0, 0, -0.5))
        #polygon = pv.Polygon()

        # mesh = decimated_meshes[0]
        #mesh = next(iter(decimated_meshes.items()))[1]
        #mesh2 = list(decimated_meshes.items())[1][1]
        #print(mesh.volume - mesh.volume)
        #label = [mesh.center[0] + 3, mesh.center[1] + 3, mesh.center[2]]
        #poly_label = pv.PolyData(label)

        #clip = mesh.clip_surface(tube, invert=True)
        #clip3 = mesh2.clip_surface(tube, invert=True)
        #clip2 = poly_label.clip_surface(poly_arc)
        #if clip2.number_of_points > 0:
        #    self.plotter.add_point_labels(points=poly_label.points, labels=['item_label'], point_size=20,
        #                                  font_size=36, name='label_12', reset_camera=False)
        #self.plotter.add_mesh(tube, style='wireframe', show_scalar_bar=False)
        #self.plotter.add_mesh(clip, color='green')
        #self.plotter.add_mesh(clip3, color='blue')

    '''
    ***********************
    *** Outsourced code ***
    ***********************
    '''

    # dummy object
    def load_dummy_object(self):
        self.clear_tool(use='excavation_side')
        # For the clipping algorithm to work, a mesh, where the plane/box widget can itself attach to, must preexist.
        # Therefore an invisible dummy is created.
        excavation_layers['dummy_layer_0'] = self.plotter.add_mesh(mesh=next(iter(decimated_meshes.items()))[1],
                                                                   name='dummy_layer_0', opacity=0.0,
                                                                   show_scalar_bar=False, reset_camera=False)

    # clear tools
    def clear_tool(self, use: str, tex_or_col='_'):
        if use == 'excavation_side':
            self.plotter.remove_actor(excavation_layers.keys())
            excavation_layers.clear()
        else:
            self.plotter.reset_camera()
            if use == 'segmentation_tool':
                if tex_or_col == 'tex':
                    self.segmentation_tool_color.setChecked(False)
                if tex_or_col == 'col':
                    self.segmentation_tool_textures.setChecked(False)
                self.plotter.clear_plane_widgets()
            if use == 'extraction_tool':
                if tex_or_col == 'tex':
                    self.extraction_tool_color.setChecked(False)
                if tex_or_col == 'col':
                    self.extraction_tool_textures.setChecked(False)
                self.plotter.clear_box_widgets()

    # clipping
    def clipping(self, use: str, param: []):
        colors = ['blue', 'green', 'red', 'yellow']

        self.plotter.remove_actor(clipped_layers_seg_ex.keys())
        clipped_layers_seg_ex.clear()

        for idx, elem in enumerate(decimated_meshes.values()):
            name = "clipped_layer_%d" % idx
            if use == 'segmentation':
                clipped_layers_seg_ex[name] = elem.clip(normal=param[0], origin=param[1], inplace=False)
            elif use == 'extraction':
                clipped_layers_seg_ex[name] = elem.clip_box(param[0].bounds, invert=False)

        if extraction_semaphor[0] == 0 or segmentation_semaphor[0] == 0:
            for tex, name in zip(textures, clipped_layers_seg_ex.keys()):
                excavation_layers[name] = self.plotter.add_mesh(mesh=clipped_layers_seg_ex[name], texture=tex, name=name,
                                                                show_scalar_bar=False, reset_camera=False)
        elif extraction_semaphor[0] == 1 or segmentation_semaphor[0] == 1:
            for col, name in zip(colors, clipped_layers_seg_ex.keys()):
                excavation_layers[name] = self.plotter.add_mesh(mesh=clipped_layers_seg_ex[name], color=col, name=name,
                                                                show_scalar_bar=False, reset_camera=False)

        if self.labels.isChecked():
            self.check_labels()

    def check_labels(self, colored=None):
        checked_seg_ex = [
            self.segmentation_tool_textures.isChecked(),
            self.segmentation_tool_color.isChecked(),
            self.extraction_tool_textures.isChecked(),
            self.extraction_tool_color.isChecked(),
        ]

        checked_shp = [
            self.shapefile_tool_textures.isChecked(),
            self.shapefile_tool_color.isChecked()
        ]

        visible_labels = {}
        points_poly = pv.PolyData(label_coordinates)

        self.plotter.remove_actor(labels.keys())
        labels.clear()

        if not any(checked_seg_ex) and not any(checked_shp) and not clipped_layers_seg_ex and not clipped_layers_shp:
            item = next(iter(decimated_meshes.items()))[1]
            box = pv.Box(item.bounds)
        if not any(checked_shp) and not clipped_layers_shp:
            box = pv.Box(clipped_layers_seg_ex['clipped_layer_0'].bounds)
        if not any(checked_seg_ex) and not clipped_layers_seg_ex:
            box = shapefiles[0].fill_holes(100)

        select = points_poly.select_enclosed_points(box)
        points_inside_box = select['SelectedPoints']

        # show/hide checkboxes
        count_dooku = 0
        for elem in points_inside_box:
            if elem == 0:
                self.hide_checkbox(count_dooku)
                count_dooku += 1
            if elem == 1:
                self.show_checkbox(count_dooku)
                count_dooku += 1

        for selected, point, name in zip(points_inside_box, label_coordinates, label_names):
            if selected == 1:
                visible_labels[name] = point

        if 1 in points_inside_box:
            for idx, key in enumerate(visible_labels):
                name = 'label_{}'.format(idx)
                color = 'white'
                if colored_labels:
                    for elem in colored_labels:
                        if key == elem:
                            color = 'green'
                labels[name] = self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key],
                                                             point_size=20, font_size=36, name=name,
                                                             reset_camera=False, text_color=color, fill_shape=False)


def colonia_4d():
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
