import sys

# Setting the Qt bindings for QtPy
import os
import numpy as np
from qtpy import QtWidgets, QtGui, QtCore
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow

os.environ["QT_API"] = "pyqt5"


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

        # allow adding a sphere
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QtWidgets.QAction('Add Mesh', self)
        self.add_sphere_action.triggered.connect(self.add_mesh)
        meshMenu.addAction(self.add_sphere_action)

        if show:
            self.show()

    def add_mesh(self):
        """ add a sphere to the pyqt frame """
        sphere = pv.Sphere()
        # self.plotter.add_mesh(sphere, show_edges=False)
        self.plotter.add_mesh_clip_box(sphere, color='white')
        self.plotter.reset_camera()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())
