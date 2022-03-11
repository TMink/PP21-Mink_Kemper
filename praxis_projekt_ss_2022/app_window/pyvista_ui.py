import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QScrollArea, QMenu
import pyvista as pv
from pyvistaqt import QtInteractor
from app_functions.search_for_format import search_for_format
from app_functions.search_texture import get_textures

os.environ["QT_API"] = "pyqt5"

DECIMATED_PATH = 'resources/models/shift_coords/ply_format/decimated/'

# lists of actor names (str)
excavation_actors = []
label_actors = []
clipped_actors = []
interaction_actors = []

# lists of plottet meshes (VTK)
plottet_actors = []
plottet_interaction_actors = []

interaction_style = [0]
all_labels = []
decimated_meshes = []
textures = []
ball = [2]


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
        elem.translate((x, y, z))
        print(elem.center)
        elem.rotate_z(50.0)


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
        right_widget = QVBoxLayout()

        # pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)

        self.plotter.add_background_image('resources/assets/colonia_4d_background.png')


        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # Label
        self.info_panel = QLabel()
        self.info_panel.setStyleSheet(open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
        self.info_panel.setFont(QFont('helvetiker regular', 15))
        self.info_panel.setText('Hello World')
        self.info_panel.setAutoFillBackground(True)
        self.info_panel.setFixedWidth(500)
        self.info_panel.hide()
        right_widget.addWidget(self.info_panel, alignment=QtCore.Qt.AlignTop)

        # checkbox
        check_boxes = []
        for i in range(0, 20):
            check_boxes.append(QCheckBox('Label'))

        for elem in check_boxes:
            elem.setStyleSheet(open('resources/style_sheets/checkbox_style_sheet.txt').read().replace('\n', ''))
            elem.setFont(QFont('helvetiker regular', 10))
            elem.setFixedWidth(440)
            elem.stateChanged.connect(self.check_box_action)

        # scroll area
        self.scroll = QScrollArea()
        self.scroll.setStyleSheet(open('resources/style_sheets/scroll_area_style_sheet.txt').read().replace('\n', ''))
        self.scroll.verticalScrollBar().setStyleSheet(
            open('resources/style_sheets/vertical_scroll_bar_style_sheet.txt').read().replace('\n', ''))
        self.scroll.setFixedWidth(500)
        self.scrollContent = QWidget(self.scroll)
        self.scrollLayout = QVBoxLayout(self.scrollContent)
        self.scrollContent.setLayout(self.scrollLayout)
        for elem in check_boxes:
            self.scrollLayout.addWidget(elem)
        self.scroll.setWidget(self.scrollContent)
        self.scroll.hide()
        right_widget.addWidget(self.scroll)
        vlayout.addLayout(right_widget)

        '''
        *** Menu Bar ***
            -> File
                -> Exit button
            -> Mesh
                -> load excavation side
                -> mesh segmentation tool
                    -> textures
                    -> color
                -> add a custom mesh for interaction
            -> Label
                -> show/hide label
                -> show/hide label side bar 
        '''
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

        # ** Mesh Menu **
        mesh_menu = main_menu.addMenu('Mesh')
        mesh_menu.setFont(QFont('helvetiker regular', 10))

        self.excavation_side = QAction('Load excavations side', self)
        self.excavation_side.triggered.connect(self.load_excavation_side)
        mesh_menu.addAction(self.excavation_side)

        # * Segmentation Menu *
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

        self.interaction_mesh = QAction('Add intractable Mesh', self)
        self.interaction_mesh.triggered.connect(self.load_interaction_mesh)
        mesh_menu.addAction(self.interaction_mesh)

        # ** Label Menu **
        label_menu = main_menu.addMenu('Labels')
        label_menu.setFont(QFont('helvetiker regular', 10))

        self.labels = QAction('Load Labels', self, checkable=True)
        self.labels.setStatusTip('Load Labels')
        self.labels.setChecked(False)
        self.labels.triggered.connect(self.load_labels)
        label_menu.addAction(self.labels)

        self.panel = QAction('Info Panel', self, checkable=True)
        self.panel.setStatusTip('Info Panel')
        self.panel.setChecked(False)
        self.panel.triggered.connect(self.hide_show)
        label_menu.addAction(self.panel)

        # key events
        self.plotter.add_key_event('m', self.interaction_mode)

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

    # makes interaction with every actor possible
    def interaction_mode(self):
        if interaction_style[0] == 0 and interaction_actors:
            self.plotter.enable_trackball_actor_style()
            self.plotter.pickable_actors = plottet_interaction_actors
            interaction_style[0] = 1
        elif interaction_style[0] == 1 and interaction_actors:
            self.plotter.enable_trackball_style()
            self.plotter.pickable_actors = plottet_interaction_actors + plottet_actors
            interaction_style[0] = 0

    # hides/shows the interactable sidepanel
    def hide_show(self):
        if self.info_panel.isHidden() and self.scroll.isHidden():
            self.info_panel.show()
            self.scroll.show()
        else:
            self.info_panel.hide()
            self.scroll.hide()

    # custom object
    def load_interaction_mesh(self):
        if excavation_actors:
            interaction_actors.clear()
            plottet_interaction_actors.clear()
            mesh = pv.Cube()
            name = 'Cube'
            mesh.translate(decimated_meshes[0].center, inplace=True)
            plottet_interaction_actors.append(self.plotter.add_mesh(mesh=mesh, name=name))
            interaction_actors.append(name)

    # excavation side segments
    def load_excavation_side(self):
        self.plotter.remove_actor(excavation_actors)
        self.plotter.remove_actor(clipped_actors)
        self.plotter.clear_plane_widgets()
        self.segmentation_tool_textures.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        plottet_actors.clear()
        excavation_actors.clear()
        if decimated_meshes:
            count = 0
            for elem, tex in zip(decimated_meshes, textures):
                name = 'excavation_%d' % count
                plottet_actors.append(self.plotter.add_mesh(mesh=elem, name=name, texture=tex))
                count += 1
                excavation_actors.append(name)
        self.plotter.reset_camera()

    # all given labels
    def load_labels(self, state):
        points = [decimated_meshes[0].center]
        labels = ['First Labels']
        if state:
            count = 0
            name = 'label_%d' % count
            self.plotter.add_point_labels(points=points, labels=labels, point_size=20, font_size=36, name=name)
            label_actors.append(name)
        else:
            self.plotter.remove_actor(label_actors)

    # segmentation tool
    def load_segmentation_tool(self, state):

        plottet_actors.clear()
        self.plotter.remove_actor(excavation_actors)
        excavation_actors.clear()

        count1 = 0
        for elem in decimated_meshes:
            name = 'excavation_%d' % count1
            self.plotter.add_mesh(mesh=elem, name=name, opacity=0.0, show_scalar_bar=False, reset_camera=False)
            count1 += 1
            excavation_actors.append(name)

        def callback_clip_mesh(normal, origin):

            clipped_meshes = []
            colors = ['blue', 'green', 'red', 'yellow']
            count = 0

            clipped_actors.clear()

            for elem in decimated_meshes:
                clipped_meshes.append(elem.clip(normal=normal, origin=origin))
                clipped_actors.append("clipped_%d" % count)
                count += 1

            self.plotter.remove_actor(clipped_actors)

            if ball[0] == 0:
                for clip, tex, name in zip(clipped_meshes, textures, clipped_actors):
                    plottet_actors.append(self.plotter.add_mesh(mesh=clip, texture=tex, name=name,
                                                                show_scalar_bar=False, reset_camera=False))
            elif ball[0] == 1:
                for clip, col, name in zip(clipped_meshes, colors, clipped_actors):
                    plottet_actors.append(self.plotter.add_mesh(mesh=clip, color=col, name=name,
                                                                show_scalar_bar=False, reset_camera=False))

        if state:

            if self.segmentation_tool_textures.isChecked() and ball[0] != 0:
                ball[0] = 0
                self.plotter.reset_camera()
                self.segmentation_tool_color.setChecked(False)
                self.plotter.clear_plane_widgets()
                self.plotter.add_plane_widget(callback_clip_mesh)
            elif self.segmentation_tool_color.isChecked() and ball[0] != 1:
                ball[0] = 1
                self.plotter.reset_camera()
                self.segmentation_tool_textures.setChecked(False)
                self.plotter.clear_plane_widgets()
                self.plotter.add_plane_widget(callback_clip_mesh)
            else:
                self.plotter.add_plane_widget(callback_clip_mesh)
        else:
            self.plotter.clear_plane_widgets()


def colonia_4d():
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
