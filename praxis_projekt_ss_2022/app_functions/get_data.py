# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import pyvista as pv

from app_functions.search_for_format import search_for_format

DECIMATED_PATH = 'resources/models/shift_coords/ply_format/decimated/'
JPG_PATH = 'resources/models/shift_coords/ply_format/'
VTK_PATH = 'resources/vtks/'


def get_decimated_meshes(dm_dict: dict):
    decimated_meshes = search_for_format(DECIMATED_PATH, ['ply'], cut=False)
    for elem in decimated_meshes:
        layer_data = elem.split(" ")
        dm_dict[layer_data[0]] = pv.read(DECIMATED_PATH + elem)


def get_textures(t_list: list):
    textures = search_for_format(JPG_PATH, ['jpg'], cut=False)
    for elem in textures:
        t_list.append(pv.read_texture(JPG_PATH + elem))


def get_shapefiles(sf_list: list):
    shapefiles = search_for_format(VTK_PATH, ['vtk'], cut=False)
    for elem in shapefiles:
        grid = pv.read(VTK_PATH + elem)
        grid_surface = grid.extract_surface()
        poly_data = pv.PolyData(grid_surface)
        sf_list.append(poly_data)
