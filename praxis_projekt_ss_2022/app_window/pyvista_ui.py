import sys
import os
from qtpy import QtWidgets
import pyvista as pv
from pyvistaqt import QtInteractor, MainWindow
from app_functions.mesh_downsample import mesh_downsample

os.environ["QT_API"] = "pyqt5"

'''
full_mesh structur:
    [0] = plotted function
    [1] = full mesh
    [2 - _] = singel parts of full mesh, in order of addition
'''
full_mesh = []

count = [0]

# Example for mesh
new_mesh = pv.read('../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.ply')
tex = pv.read_texture('../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.jpg')

all_meshes = mesh_downsample()

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
        # clear the box_widget, if one exist
        print(count[0])
        self.plotter.clear_box_widgets()
        target_reduction = 0.9
        mesh = all_meshes[0]
        #mesh = mesh.decimate_pro(target_reduction, preserve_topology=True)
        if full_mesh:
            merged = full_mesh[1].merge(mesh)
            full_mesh[0] = (self.plotter.add_mesh(merged, texture=tex))
            full_mesh[1] = merged
            full_mesh.append(mesh)
        else:
            full_mesh.append(self.plotter.add_mesh(mesh, texture=tex))
            full_mesh.append(mesh)
            full_mesh.append(mesh)
        count[0] += 1
        self.plotter.reset_camera()

    # adds a mesh clip box
    def add_mesh_box_func(self):
        if full_mesh:
            mesh_full = full_mesh[1]
            self.plotter.clear()
            full_mesh.append(self.plotter.add_mesh_clip_box(mesh_full, name='mesh_with_box', texture=tex))
        else:
            print("Error, no mesh loaded")


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    sys.exit(app.exec_())
