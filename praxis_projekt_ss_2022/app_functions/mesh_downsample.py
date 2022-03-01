import pyvista as pv
from app_functions.search_for_format import search_for_format

PLY_PATH = '../models/shift_coords/ply_format/'


def mesh_downsample():
    target_reduction = 0.9
    downsampled = []
    ply_list = search_for_format(PLY_PATH, ['ply'])
    print(ply_list)

    for elem in ply_list:
        mesh = pv.read(PLY_PATH + elem)
        downsampled.append(mesh.decimate_pro(target_reduction, preserve_topology=True))

    return downsampled
