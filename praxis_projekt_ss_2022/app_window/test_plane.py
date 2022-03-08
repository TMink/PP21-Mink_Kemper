import pyvista as pv
import pymeshfix as mf
import open3d as o3d

from app_functions.mesh_downsample import mesh_downsample
from app_functions.search_texture import get_textures

p = pv.Plotter()

'''
mesh_one = pv.read('../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.ply')
mesh_two = pv.read('../models/shift_coords/ply_format/17-07 SE07005+006+007+008+010+011+012+013+014+015.ply')

texture_one = pv.read_texture(
    '../models/shift_coords/ply_format/15_17-07 SE07011+012+013+014+015+016+017+018+019+020.jpg')
# texture_two = pv.read_texture('../models/shift_coords/ply_format/17-07 SE07005+006+007+008+010+011+012+013+014+015.jpg')

# p.add_mesh(mesh_one, color='red')
# p.add_mesh(mesh_two, color='blue')

sphere = pv.Sphere()
cube = pv.Cube()
new_cube = pv.Cube()
new_cube.translate((0, 1, 0))
plane = pv.Plane()
plane.rotate_x(90)

mesh_one.rotate_z(50.0)
mesh_two.rotate_z(50.0)
p.add_mesh(mesh_one, opacity=0.0)
p.remove_scalar_bar()


def func(normal, origin):
    clipped = mesh_one.clip(normal=normal, origin=origin)
    clipped2 = mesh_two.clip(normal=normal, origin=origin)
    p.remove_actor("test")
    p.remove_actor("test2")
    p.add_mesh(clipped, color='blue', name="test")
    p.add_mesh(clipped2, color='red', name="test2")


p.add_plane_widget(func)

names = []
count = 0

names.append("mesh%d" % count)
count += 1
names.append("mesh%d" % count)

print(names)
'''

downsampled_meshes = []
plottet_mesh = []
textures = []

downsampled = mesh_downsample()
for elem in downsampled:
    downsampled_meshes.append(elem)

for elem in downsampled_meshes:
    elem.rotate_z(50.0)

tex = get_textures()
for elem2 in tex:
    textures.append(elem2)

if downsampled_meshes:
    for elem, tex in zip(downsampled_meshes, textures):
        plottet_mesh.append(p.add_mesh(elem, name='full_mesh', texture=tex))


def add_new_plane(state):
    p.add_mesh(downsampled_meshes[0], opacity=0.0)

    def test_func(normal, origin):

        clipped_meshes = []
        actors_names = []
        colors = ['blue', 'green']
        names = []
        count = 0

        for elem in downsampled_meshes:
            clipped_meshes.append(elem.clip(normal=normal, origin=origin))
            names.append("mesh%d" % count)
            count += 1

        for name in names:
            p.remove_actor(name)

        for clip, col, name in zip(clipped_meshes, colors, names):
            p.add_mesh(mesh=clip, color=col, name=name)

    if state:
        for elem in plottet_mesh:
            p.remove_actor(elem)
        plottet_mesh.append(p.add_plane_widget(test_func))
    else:
        p.clear_plane_widgets()


add_new_plane(True)

p.reset_camera()
p.show()
