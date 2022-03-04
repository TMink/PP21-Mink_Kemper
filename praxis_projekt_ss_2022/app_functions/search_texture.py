from app_functions.search_for_format import search_for_format
import pyvista as pv

JPG_PATH = 'models/shift_coords/ply_format/'


def get_textures():
    textures = search_for_format(JPG_PATH, ['jpg'], cut=False)
    textures_read = []
    for elem in textures:
        textures_read.append(pv.read_texture(JPG_PATH + elem))
    return textures_read
