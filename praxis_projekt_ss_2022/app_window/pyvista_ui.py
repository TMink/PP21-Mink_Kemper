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

'''
plottet_mesh:
    [0] = plottet full mesh

actors:
    [0] = plottet added mesh
    [1] = added mesh
'''
plottet_mesh = []
actors = []
interaction_style = [0]
all_labels = []
downsampled_meshes = []
textures = []


def get_data():
    downsampled = mesh_downsample()
    tex = get_textures()
    for elem in downsampled:
        downsampled_meshes.append(elem)
    for elem2 in tex:
        textures.append(elem2)


def merge_segments():
    merged_segemnts = []
    for elem in downsampled_meshes:
        if merged_segemnts:
            merged = merged_segemnts[0].merge(elem)
            merged_segemnts[0] = merged
        else:
            merged_segemnts.append(elem)
    return merged_segemnts


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
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a mesh and clip box
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_mesh = QAction('Add Mesh', self)
        self.add_mesh.triggered.connect(self.add_mesh_func)
        meshMenu.addAction(self.add_mesh)

        self.add_mesh_box = QAction('Mesh Segmentation', self, checkable=True)
        self.add_mesh_box.setStatusTip('Mesh Segmentation')
        self.add_mesh_box.setChecked(False)
        self.add_mesh_box.triggered.connect(self.add_mesh_box_func)
        meshMenu.addAction(self.add_mesh_box)

        self.load_mesh = QAction('Load all Segments', self)
        self.load_mesh.triggered.connect(self.load_mesh_func)
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
        self.checkbox_1.stateChanged.connect(self.check_box_change_action)
        right_widget.addWidget(self.checkbox_1, alignment=QtCore.Qt.AlignTop)
        vlayout.addLayout(right_widget)

        # key events
        self.plotter.add_key_event('p', self.hide_show)
        self.plotter.add_key_event('m', self.change_interaction_mode)

        if show:
            self.show()

    # check bos in side panel
    def check_box_change_action(self, state):
        if QtCore.Qt.Checked == state:
            self.change_interaction_mode()
        else:
            self.change_interaction_mode()

    # makes interaction with every actor possible
    def change_interaction_mode(self):
        if interaction_style[0] == 0:
            self.plotter.enable_trackball_actor_style()
            self.plotter.pickable_actors = [actors[0]]
            interaction_style[0] = 1
        else:
            self.plotter.enable_trackball_style()
            self.plotter.pickable_actors = [actors[0], plottet_mesh[0]]
            interaction_style[0] = 0

    # hides/shows the interactable sidepanel
    def hide_show(self):
        if self.label.isHidden() and self.checkbox_1.isHidden():
            self.label.show()
            self.checkbox_1.show()
        else:
            self.label.hide()
            self.checkbox_1.hide()

    # creates a new mesh and merge it, if one already exist
    def add_mesh_func(self):
        if plottet_mesh:
            mesh = pv.Sphere()
            mesh.translate(downsampled_meshes[0].center, inplace=True)
            actors.append(self.plotter.add_mesh(mesh, name='sphere'))
            actors.append(mesh)

    # adds a mesh clip box
    def add_mesh_box_func(self, state):
        if plottet_mesh:
            merged_segments = merge_segments()
            if state:
                for elem in plottet_mesh:
                    self.plotter.remove_actor(elem)
                plottet_mesh.append(self.plotter.add_mesh_clip_box(merged_segments[0], name='mesh_with_box', color='blue'))
            else:
                self.plotter.clear_box_widgets()

    # loads the segments
    def load_mesh_func(self):
        if plottet_mesh:
            for elem in plottet_mesh:
                self.plotter.remove_actor(elem)
        if downsampled_meshes:
            for elem, tex in zip(downsampled_meshes, textures):
                plottet_mesh.append(self.plotter.add_mesh(elem, name='full_mesh', texture=tex))
        self.plotter.reset_camera()

    # loads all given labels
    def load_labels(self, state):
        points = [downsampled_meshes[0].center]
        labels = ['First Labels']
        if state:
            self.plotter.add_point_labels(points, labels, point_size=20, font_size=36, name='points')
        else:
            self.plotter.remove_actor('points')


def colonia_4d():
    app = QApplication(sys.argv)
    MyMainWindow()
    sys.exit(app.exec_())
