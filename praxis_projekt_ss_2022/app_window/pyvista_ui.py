import sys

# Setting the Qt bindings for QtPy
import os
import numpy as np
from qtpy import QtWidgets, QtGui, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow

os.environ["QT_API"] = "pyqt5"

meshes = []
actors = []
count = [0]


class MyMainWindow(MainWindow):

    def __init__(self, parent=None, show=True):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = QtWidgets.QFrame()
        vlayout = QtWidgets.QVBoxLayout()

        # add the pyvista interactor object
        self.plotter = QtInteractor(self.frame)
        vlayout.addWidget(self.plotter.interactor)
        self.signal_close.connect(self.plotter.close)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = QtWidgets.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # allow adding a mesh and clip box
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_mesh = QtWidgets.QAction('Add Mesh', self)
        self.add_mesh.triggered.connect(self.add_mesh_func)
        meshMenu.addAction(self.add_mesh)

        self.add_mesh_box = QtWidgets.QAction('Mesh Segmentation', self)
        self.add_mesh_box.triggered.connect(self.add_mesh_box_func)
        meshMenu.addAction(self.add_mesh_box)

        if show:
            self.show()

    # creates a new mesh and merge it, if one already exist
    def add_mesh_func(self):
        """ add a sphere to the pyqt frame """
        self.plotter.clear_box_widgets()
        sphere = pv.Sphere()
        trans = sphere.translate((0, 0, count[0]), inplace=True)
        if meshes:
            merged = meshes[0].merge(trans)
            meshes[0] = merged
        else:
            meshes.append(trans)
        count[0] += 1
        if actors:
            self.plotter.remove_actor(actors[0])
            actors[0] = (self.plotter.add_mesh(meshes[0], name='mesh_{}'.format(1)))
        else:
            actors.append(self.plotter.add_mesh(meshes[0], name='mesh_{}'.format(1)))
        self.plotter.reset_camera()

    # adds a mesh clip box
    def add_mesh_box_func(self):
        if actors:
            self.plotter.remove_actor(actors[0])
            actors[0] = (self.plotter.add_mesh_clip_box(meshes[0]))
        else:
            print("Error, no mesh loaded")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())
