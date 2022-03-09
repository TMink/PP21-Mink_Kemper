import sys
import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QScrollArea, \
    QPushButton
import pyvista as pv
from pyvistaqt import QtInteractor
from app_functions.mesh_downsample import mesh_downsample
from app_functions.search_texture import get_textures

os.environ["QT_API"] = "pyqt5"

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
downsampled_meshes = []
textures = []


# downsampled meshes and textures
def get_data():
    downsampled = mesh_downsample()
    tex = get_textures()
    for elem in downsampled:
        downsampled_meshes.append(elem)
    for elem2 in tex:
        textures.append(elem2)


# rotates the downsampled meshes at an 50 degree angle around the z-axis
def transform_downsampled_meshes():
    for elem in downsampled_meshes:
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

        self.add_mesh = QAction('Add Mesh', self)
        self.add_mesh.triggered.connect(self.load_custom_object)
        mesh_menu.addAction(self.add_mesh)

        self.add_plane = QAction('Mesh Plane', self, checkable=True)
        self.add_plane.setStatusTip('Mesh Plane')
        self.add_plane.setChecked(False)
        self.add_plane.triggered.connect(self.load_segmentation_tool)
        mesh_menu.addAction(self.add_plane)

        self.load_mesh = QAction('Load all Segments', self)
        self.load_mesh.triggered.connect(self.load_excavation_side)
        mesh_menu.addAction(self.load_mesh)

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
    def load_custom_object(self):
        if excavation_actors:
            interaction_actors.clear()
            plottet_interaction_actors.clear()
            mesh = pv.Cube()
            name = 'Cube'
            mesh.translate(downsampled_meshes[0].center, inplace=True)
            plottet_interaction_actors.append(self.plotter.add_mesh(mesh=mesh, name=name))
            interaction_actors.append(name)

    # excavation side segments
    def load_excavation_side(self):
        self.plotter.remove_actor(excavation_actors)
        self.plotter.remove_actor(clipped_actors)
        self.plotter.clear_plane_widgets()
        self.add_plane.setChecked(False)
        plottet_actors.clear()
        excavation_actors.clear()
        if downsampled_meshes:
            count = 0
            for elem, tex in zip(downsampled_meshes, textures):
                name = 'excavation_%d' % count
                plottet_actors.append(self.plotter.add_mesh(mesh=elem, name=name, texture=tex))
                count += 1
                excavation_actors.append(name)
        self.plotter.reset_camera()

    # all given labels
    def load_labels(self, state):
        points = [downsampled_meshes[0].center]
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
        self.plotter.add_mesh(mesh=downsampled_meshes[0], opacity=0.0, name='dummy')
        excavation_actors.append('dummy')

        def callback_clip_mesh(normal, origin):

            clipped_meshes = []
            colors = ['blue', 'green']
            count = 0

            clipped_actors.clear()

            for elem in downsampled_meshes:
                clipped_meshes.append(elem.clip(normal=normal, origin=origin))
                clipped_actors.append("clipped_%d" % count)
                count += 1

            self.plotter.remove_actor(clipped_actors)

            # load this for colored meshes
            #for clip, col, name in zip(clipped_meshes, colors, clipped_actors):
            #    plottet_actors.append(self.plotter.add_mesh(mesh=clip, color=col, name=name))

            for clip, tex, name in zip(clipped_meshes, textures, clipped_actors):
                plottet_actors.append(self.plotter.add_mesh(mesh=clip, texture=tex, name=name))

        if state:
            self.plotter.add_plane_widget(callback_clip_mesh)
        else:
            self.plotter.clear_plane_widgets()


def colonia_4d():
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyleSheet('.QFrame{background-color:#101010}')
    w = Window()
    w.show()
    sys.exit(app.exec_())
