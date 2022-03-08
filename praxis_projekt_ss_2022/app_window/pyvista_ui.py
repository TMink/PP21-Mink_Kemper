import sys
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QApplication
from qtpy import QtWidgets, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
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


class MyMainWindow(MainWindow, QWidget):

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QFrame()

        width = 1500
        height = 900
        self.setMinimumSize(width, height)

        # whole body
        vlayout = QHBoxLayout()

        # right side
        right_widget = QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        exit_button = QAction('Exit', self)
        exit_button.setShortcut('Ctrl+Q')
        exit_button.triggered.connect(self.close)
        file_menu.addAction(exit_button)

        # allow adding a mesh and clip box
        meshMenu = main_menu.addMenu('Mesh')
        self.add_mesh = QAction('Add Mesh', self)
        self.add_mesh.triggered.connect(self.load_custom_object)
        meshMenu.addAction(self.add_mesh)

        self.add_plane = QAction('Mesh Plane', self, checkable=True)
        self.add_plane.setStatusTip('Mesh Plane')
        self.add_plane.setChecked(False)
        self.add_plane.triggered.connect(self.load_segmentation_tool)
        meshMenu.addAction(self.add_plane)

        self.load_mesh = QAction('Load all Segments', self)
        self.load_mesh.triggered.connect(self.load_excavation_side)
        meshMenu.addAction(self.load_mesh)

        self.load_the_labels = QAction('Load Labels', self, checkable=True)
        self.load_the_labels.setStatusTip('Load Labels')
        self.load_the_labels.setChecked(False)
        self.load_the_labels.triggered.connect(self.load_labels)
        meshMenu.addAction(self.load_the_labels)

        # toolbar
        # exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        # exitAct.setShortcut('Ctrl+Q')
        # exitAct.triggered.connect(qApp.quit)
        # self.toolbar = self.addToolBar('Exit')
        # self.toolbar.addAction(exitAct)

        # Label
        self.label = QLabel()
        self.label.setText('Hello World')
        self.label.setAutoFillBackground(True)
        self.label.setFixedWidth(500)
        self.label.setFixedHeight(450)
        self.label.setStyleSheet("border: 3px solid black;")
        right_widget.addWidget(self.label, alignment=QtCore.Qt.AlignTop)

        # checkbox
        self.checkbox_1 = QCheckBox('Interaction Mode')
        self.checkbox_1.stateChanged.connect(self.check_box_action)
        right_widget.addWidget(self.checkbox_1, alignment=QtCore.Qt.AlignTop)
        vlayout.addLayout(right_widget)

        # key events
        self.plotter.add_key_event('p', self.hide_show)
        self.plotter.add_key_event('m', self.interaction_mode)

        if show:
            self.show()

    # check box in side panel
    def check_box_action(self, state):
        if QtCore.Qt.Checked == state:
            self.interaction_mode()
        else:
            self.interaction_mode()

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
        if self.label.isHidden() and self.checkbox_1.isHidden():
            self.label.show()
            self.checkbox_1.show()
        else:
            self.label.hide()
            self.checkbox_1.hide()

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
    app = QApplication(sys.argv)
    MyMainWindow()
    sys.exit(app.exec_())
