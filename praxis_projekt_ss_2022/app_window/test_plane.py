import pyvista as pv
import numpy as np

points = [(1.0, 1.0, 1.0)]
labels = ['First Labels']

p = pv.Plotter()
p.add_point_labels(points, labels, point_size=20, font_size=36)
p.reset_camera()
p.show()
