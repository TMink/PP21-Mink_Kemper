import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QScrollArea, QMenu, \
    QPushButton, QSpacerItem, QSizePolicy
import pyvista as pv
from pyvistaqt import QtInteractor
from app_functions.search_for_format import search_for_format
from app_functions.search_texture import get_textures

os.environ["QT_API"] = "pyqt5"

DECIMATED_PATH = 'resources/models/shift_coords/ply_format/decimated/'

# lists of actor names (str)
excavation_actors = []
label_actors = []
clipped_mesh_actors = []
interaction_actors = []

# lists of plotted meshes (VTK)
plotted_actors = []
plotted_interaction_actors = []
plotted_labels = []

# list of clipped meshes
clipped_meshes = []

# semaphores
segmentation_semaphor = [2]
extraction_semaphor = [2]

interaction_style = [0]
all_labels = []
decimated_meshes = []
textures = []
label_points = []
label_names = []


# get decimated meshes and textures
def get_data():
    meshes = search_for_format(DECIMATED_PATH, ['ply'], cut=False)
    tex = get_textures()
    for elem in meshes:
        decimated_meshes.append(pv.read(DECIMATED_PATH + elem))
    for elem2 in tex:
        textures.append(elem2)


# rotates the downsampled meshes at an 50 degree angle around the z-axis
def transform_downsampled_meshes():
    x = decimated_meshes[0].center[0] * -1.0
    y = decimated_meshes[0].center[1] * -1.0
    z = decimated_meshes[0].center[2] * -1.0
    for elem in decimated_meshes:
        elem.translate((x, y, z), inplace=True)
        elem.rotate_z(50.0, inplace=True)

    # labels
    hello_there = decimated_meshes[0].center
    hello_again = [decimated_meshes[0].center[0] + 1, decimated_meshes[0].center[1], decimated_meshes[0].center[0]]
    label_points.append(hello_there)
    label_points.append(hello_again)
    label_names.append('Hello there!')
    label_names.append('Hello again!')


# Ui setup
class UiMainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.setWindowTitle('MainWindow')
        MainWindow.resize(1500, 900)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName('centralWidnget')
        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


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

        self.plotter.add_background_image('resources/assets/colonia_4d_background.png')

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        '''
        **************************************
        *** Label info panel (ui settings) ***
        **************************************
        '''
        # Label
        self.info_panel = QLabel()
        self.info_panel.setStyleSheet(open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
        self.info_panel.setFont(QFont('helvetiker regular', 15))
        self.info_panel.setText('Hello World')
        self.info_panel.setAutoFillBackground(True)
        self.info_panel.setFixedWidth(500)
        self.info_panel.hide()
        panels.addWidget(self.info_panel, alignment=QtCore.Qt.AlignTop)

        # checkbox
        self.check_boxes = []
        for i in range(0, len(label_points)):
            checkbox = QCheckBox(label_names[i])
            checkbox.setObjectName('checkbox_%d' % i)
            self.check_boxes.append(checkbox)

        for elem in self.check_boxes:
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
        for elem in self.check_boxes:
            self.scroll_labels_Layout.addWidget(elem)
        self.spacer_item = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_labels_Layout.addItem(self.spacer_item)
        self.scroll_labels.setWidget(self.scroll_labels_Content)
        self.scroll_labels.hide()
        panels.addWidget(self.scroll_labels)

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
                -> load excavation side
                -> mesh segmentation tool
                    -> load mesh with original textures
                    -> load mesh with segment colors
                -> add a custom mesh for interaction
            -> Interactable Objects
                -> shows/hides objects
                -> show/hide objects info panel
            -> Label
                -> shows/hides labels
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

        self.exit_button = QAction('Exit', self)
        self.exit_button.setShortcut('Ctrl+Q')
        self.exit_button.triggered.connect(self.close)
        file_menu.addAction(self.exit_button)

        # ** Mesh **
        mesh_menu = main_menu.addMenu('Tools')
        mesh_menu.setFont(QFont('helvetiker regular', 10))

        # * Load excavation side *
        self.excavation_side = QAction('Load excavations side', self)
        self.excavation_side.triggered.connect(self.load_excavation_side)
        mesh_menu.addAction(self.excavation_side)

        # * Mesh segmentation tool *
        self.segmentation_menu = QMenu('Segmentation Tool')
        self.segmentation_menu.setStyleSheet(
            open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

        self.segmentation_tool_textures = QAction('With textures', self, checkable=True)
        self.segmentation_tool_textures.setStatusTip('With textures')
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_textures.triggered.connect(self.load_segmentation_tool)

        self.segmentation_tool_color = QAction('With color', self, checkable=True)
        self.segmentation_tool_color.setStatusTip('With color')
        self.segmentation_tool_color.setChecked(False)
        self.segmentation_tool_color.triggered.connect(self.load_segmentation_tool)

        self.segmentation_menu.addAction(self.segmentation_tool_textures)
        self.segmentation_menu.addAction(self.segmentation_tool_color)
        mesh_menu.addMenu(self.segmentation_menu)

        # * Mesh extraction tool *
        self.extraction_menu = QMenu('Extraction Tool')
        self.extraction_menu.setStyleSheet(
            open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

        self.extraction_tool_textures = QAction('With textures', self, checkable=True)
        self.extraction_tool_textures.setStatusTip('With textures')
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_textures.triggered.connect(self.load_extraction_tool)

        self.extraction_tool_color = QAction('With color', self, checkable=True)
        self.extraction_tool_color.setStatusTip('With color')
        self.extraction_tool_color.setChecked(False)
        self.extraction_tool_color.triggered.connect(self.load_extraction_tool)

        self.extraction_menu.addAction(self.extraction_tool_textures)
        self.extraction_menu.addAction(self.extraction_tool_color)
        mesh_menu.addMenu(self.extraction_menu)

        # * Add a custom mesh for interaction *
        self.interaction_mesh = QAction('Add intractable Mesh', self)
        self.interaction_mesh.triggered.connect(self.load_interaction_mesh)
        mesh_menu.addAction(self.interaction_mesh)

        # ** Label **
        label_menu = main_menu.addMenu('Labels')
        label_menu.setFont(QFont('helvetiker regular', 10))

        # * Shows/Hides labels *
        self.labels = QAction('Load Labels', self, checkable=True)
        self.labels.setStatusTip('Load Labels')
        self.labels.setChecked(False)
        self.labels.triggered.connect(self.load_labels)
        label_menu.addAction(self.labels)

        # * Shows/Hides label info panel *
        self.panel = QAction('Info Panel', self, checkable=True)
        self.panel.setStatusTip('Info Panel')
        self.panel.setChecked(False)
        self.panel.triggered.connect(self.hide_show_label_info_side_panel)
        label_menu.addAction(self.panel)

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

        self.plotter.add_key_event('m', self.interaction_mode)

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

    # shows the element and adds a new spacer_item
    def show_checkbox(self, pos):
        self.scroll_labels_Layout.removeItem(self.spacer_item)
        for elem in self.check_boxes:
            if elem.objectName() == 'checkbox_%d' % pos:
                elem.show()
        self.scroll_labels_Layout.addItem(self.spacer_item)

    # hides a checkbox
    def hide_checkbox(self, pos):
        for elem in self.check_boxes:
            if elem.objectName() == 'checkbox_%d' % pos:
                elem.hide()

    # emits a signal is window is manually resized
    def resizeEvent(self, event):
        self.resized.emit()
        return super(Window, self).resizeEvent(event)

    # updates the height of the info panel in comparison to the actual window height
    def update_height(self):
        self.info_panel.setFixedHeight(self.height() / 2)

    # check box in side panel
    def check_box_action(self, state):
        if QtCore.Qt.Checked == state:
            self.interaction_mode()
            self.info_panel.setText('Interactionmode On')
        else:
            self.interaction_mode()
            self.info_panel.setText('Interactionmode Off')

    # hides/shows the interactable sidepanel
    def hide_show_label_info_side_panel(self):
        if self.info_panel.isHidden() and self.scroll_labels.isHidden():
            self.info_panel.show()
            self.scroll_labels.show()
            self.scroll_interactable_objects.hide()
        else:
            self.info_panel.hide()
            self.scroll_labels.hide()
            self.panel.setChecked(False)

    # hides/shows the interactable sidepanel
    def hide_show_interaction_side_panel(self):
        if self.scroll_interactable_objects.isHidden():
            self.scroll_interactable_objects.show()
            self.info_panel.hide()
            self.scroll_labels.hide()
            self.panel.setChecked(False)
        else:
            self.scroll_interactable_objects.hide()

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
            self.plotter.pickable_actors = plotted_interaction_actors + plotted_actors
            interaction_style[0] = 0

    '''
    **************************************
    *** Loading/Manipulation of meshes ***
    **************************************
    '''

    # custom object
    def load_interaction_mesh(self):
        if excavation_actors or clipped_mesh_actors:
            interaction_actors.clear()
            plotted_interaction_actors.clear()
            self.hide_show_interaction_side_panel()
            mesh = pv.Cube()
            name = 'Cube'
            mesh.translate(decimated_meshes[0].center, inplace=True)
            plotted_interaction_actors.append(self.plotter.add_mesh(mesh=mesh, name=name))
            interaction_actors.append(name)

    # excavation side segments
    def load_excavation_side(self):

        # clear and reset
        self.plotter.remove_actor(excavation_actors)
        self.plotter.remove_actor(clipped_mesh_actors)
        self.plotter.clear_plane_widgets()
        self.plotter.clear_box_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        self.plotter.reset_camera()
        plotted_actors.clear()
        excavation_actors.clear()

        if self.labels.isChecked():
            self.check_labels()
        if decimated_meshes:
            count = 0
            for elem, tex in zip(decimated_meshes, textures):
                name = 'excavation_%d' % count
                plotted_actors.append(self.plotter.add_mesh(mesh=elem, name=name, texture=tex))
                count += 1
                excavation_actors.append(name)

    # all given labels
    def load_labels(self, state):
        if state:
            if excavation_actors or clipped_mesh_actors:
                self.check_labels()
        else:
            self.plotter.remove_actor(label_actors)

    # segmentation tool
    def load_segmentation_tool(self, state):

        # clear and reset
        self.plotter.clear_box_widgets()
        self.extraction_tool_textures.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        self.clear_tools()

        def clip_mesh(normal, origin):
            self.segmentation_extraction(use='segmentation', param=[normal, origin])
            extraction_semaphor[0] = 2

        if state:
            if self.segmentation_tool_textures.isChecked() and segmentation_semaphor[0] != 0:
                segmentation_semaphor[0] = 0
                self.plotter.reset_camera()
                self.segmentation_tool_color.setChecked(False)
                self.plotter.clear_plane_widgets()
                self.plotter.add_plane_widget(clip_mesh)
            elif self.segmentation_tool_color.isChecked() and segmentation_semaphor[0] != 1:
                segmentation_semaphor[0] = 1
                self.plotter.reset_camera()
                self.segmentation_tool_textures.setChecked(False)
                self.plotter.clear_plane_widgets()
                self.plotter.add_plane_widget(clip_mesh)
            else:
                self.plotter.add_plane_widget(clip_mesh)
        else:
            self.plotter.clear_plane_widgets()

    # extraction tool
    def load_extraction_tool(self, state):

        # clear and reset
        self.plotter.clear_plane_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.clear_tools()

        def clip_mesh(box):
            self.segmentation_extraction(use='extraction', param=[box])
            segmentation_semaphor[0] = 2

        if state:
            if self.extraction_tool_textures.isChecked() and extraction_semaphor[0] != 0:
                extraction_semaphor[0] = 0
                self.plotter.reset_camera()
                self.extraction_tool_color.setChecked(False)
                self.plotter.clear_box_widgets()
                self.plotter.add_box_widget(clip_mesh, rotation_enabled=False)
            elif self.extraction_tool_color.isChecked() and extraction_semaphor[0] != 1:
                extraction_semaphor[0] = 1
                self.plotter.reset_camera()
                self.extraction_tool_textures.setChecked(False)
                self.plotter.clear_box_widgets()
                self.plotter.add_box_widget(clip_mesh, rotation_enabled=False)
            else:
                self.plotter.add_box_widget(clip_mesh, rotation_enabled=False)
        else:
            #self.check_labels()
            self.plotter.clear_box_widgets()

    '''
    ***********************
    *** Outsourced code ***
    ***********************
    '''

    # clear tools
    def clear_tools(self):
        self.plotter.remove_actor(excavation_actors)
        self.plotter.remove_actor(label_actors)
        excavation_actors.clear()
        plotted_actors.clear()

        count1 = 0
        for elem in decimated_meshes:
            name = 'excavation_%d' % count1
            self.plotter.add_mesh(mesh=elem, name=name, opacity=0.0, show_scalar_bar=False, reset_camera=False)
            count1 += 1
            excavation_actors.append(name)

    # segmentation_extraction
    def segmentation_extraction(self, use: str, param: []):
        colors = ['blue', 'green', 'red', 'yellow']
        mesh_count = 0

        clipped_meshes.clear()
        clipped_mesh_actors.clear()

        for elem in decimated_meshes:
            if use == 'segmentation':
                clipped_meshes.append(elem.clip(normal=param[0], origin=param[1], inplace=False))
            elif use == 'extraction':
                clipped_meshes.append(elem.clip_box(param[0].bounds, invert=False))
            clipped_mesh_actors.append("clipped_%d" % mesh_count)
            mesh_count += 1

        self.plotter.remove_actor(clipped_mesh_actors)

        if extraction_semaphor[0] == 0 or segmentation_semaphor[0] == 0:
            for clip, tex, name in zip(clipped_meshes, textures, clipped_mesh_actors):
                plotted_actors.append(self.plotter.add_mesh(mesh=clip, texture=tex, name=name,
                                                            show_scalar_bar=False, reset_camera=False))
        elif extraction_semaphor[0] == 1 or segmentation_semaphor[0] == 1:
            for clip, col, name in zip(clipped_meshes, colors, clipped_mesh_actors):
                plotted_actors.append(self.plotter.add_mesh(mesh=clip, color=col, name=name,
                                                            show_scalar_bar=False, reset_camera=False))

        if self.labels.isChecked():
            self.check_labels()

    def check_labels(self):
        checked = [
            self.segmentation_tool_textures.isChecked(),
            self.segmentation_tool_color.isChecked(),
            self.extraction_tool_textures.isChecked(),
            self.extraction_tool_color.isChecked()
        ]

        labels_points = []
        labels_names = []
        points_poly = pv.PolyData(label_points)
        label_count = 0

        self.plotter.remove_actor(label_actors)
        label_actors.clear()

        if not any(checked):
            box = pv.Box(decimated_meshes[0].bounds)
        else:
            box = pv.Box(clipped_meshes[0].bounds)

        select = points_poly.select_enclosed_points(box)
        points_inside_box = select['SelectedPoints']

        #
        count_dooku = 0
        for elem in points_inside_box:
            if elem == 0:
                self.hide_checkbox(count_dooku)
                count_dooku += 1
            if elem == 1:
                self.show_checkbox(count_dooku)
                count_dooku += 1

        for selected, points, names in zip(points_inside_box, label_points, label_names):
            if selected == 1:
                name = 'label_%d' % label_count
                labels_points.append(points)
                labels_names.append(names)
                label_actors.append(name)
                label_count += 1

        if 1 in points_inside_box:
            for i in range(0, len(labels_points)):
                self.plotter.add_point_labels(points=[labels_points[i]], labels=[labels_names[i]],
                                              point_size=20, font_size=36, name=label_actors[i],
                                              reset_camera=False)


def colonia_4d():
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
