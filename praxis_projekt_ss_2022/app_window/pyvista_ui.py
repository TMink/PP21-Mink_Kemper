import sys
import os

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QAction, QFrame, QApplication
from qtpy import QtWidgets, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
from app_functions.mesh_downsample import mesh_downsample

os.environ["QT_API"] = "pyqt5"

'''
full_mesh structur:
    [0] = full mesh
    [1 - 00] = individual segments

actors structur:
    [0] = plottet full mesh
    [0] = 
'''
full_mesh = []
plottet_mesh = []
actors = []
interaction_style = [0]
all_labels = []

# Example for mesh
new_mesh = pv.read('../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.ply')
tex = pv.read_texture('../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.jpg')

# downsample all pre-loaded meshes
all_meshes = mesh_downsample()


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
        mesh = pv.Sphere()
        mesh.translate(full_mesh[0].center, inplace=True)
        actors.append(self.plotter.add_mesh(mesh, name='sphere'))
        actors.append(mesh)

    # adds a mesh clip box
    def add_mesh_box_func(self, state):
        if state:
            self.plotter.remove_actor(plottet_mesh[0])
            plottet_mesh.append(self.plotter.add_mesh_clip_box(full_mesh[0], name='mesh_with_box', texture=tex))
        else:
            self.plotter.remove_actor(plottet_mesh[0])
            plottet_mesh.append(self.plotter.add_mesh(full_mesh[0], name='full_mesh', texture=tex))

    # loads the full mesh with every segment
    def load_mesh_func(self):
        for elem in all_meshes:
            if full_mesh:
                merged = full_mesh[0].merge(elem)
                full_mesh[0] = merged
                full_mesh.append(elem)
            else:
                full_mesh.append(elem)
                plottet_mesh.append(self.plotter.add_mesh(elem, name='full_mesh', texture=tex))
        if full_mesh[0] is not None:
            plottet_mesh[0] = self.plotter.add_mesh(full_mesh[0], name='full_mesh', texture=tex)
        self.plotter.reset_camera()

    # loads all given labels
    def load_labels(self, state):
        points = [full_mesh[0].center]
        labels = ['First Labels']
        if state:
            self.plotter.add_point_labels(points, labels, point_size=20, font_size=36, name='points')
        else:
            self.plotter.remove_actor('points')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())
