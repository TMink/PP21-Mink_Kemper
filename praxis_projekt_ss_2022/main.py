# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import app_functions.global_shift as gs
import app_functions.obj_to_ply as otp
import app_functions.shp_to_poly as stv
import app_functions.mesh_downsample as dm
import app_functions.get_data as gd
import app_functions.general_data_manipulation as td
import app_window.pyvista_ui as ui

from data.dictionarys import *
from data.lists import *

if __name__ == '__main__':
    # perform global shift on content in utm_data and saves it in shift_corrds/ibj_format
    gs.utm_to_shift()
    print('utm_to_shift -- done')

    # converts content of shift_coords/obj_format from .obj to .ply and saves it in shift_coords/ply_format
    otp.oby_to_ply()
    print('oby_to_ply -- done')

    # converts Shapefiles into VTKs
    stv.shp_to_poly()
    print("shp_to_vtk -- done")

    # decimates the meshes in shift_coords/ply_format and saves them in shift_coords/ply_format/decimated
    dm.decimate_meshes()
    print('decimate_meshes -- done')

    # loads all converted meshes and corresponding textures
    gd.get_decimated_meshes(dm_dict=decimated_meshes)
    print('get_decimated_meshes -- done')

    # loads all converted meshes and corresponding textures
    gd.get_textures(t_list=textures)
    print('get_textures -- done')

    # loads all VTKs and saves them als PolyData
    #gd.get_shapefiles(sf_list=shapefiles)
    #print('get_shapefiles -- done')

    # rotates the content of decimated_meshes at an 50 degree angle around the z-axis
    td.rotate(data=decimated_meshes.values())
    print('rotate_downsampled_meshes -- done')

    # rotates the content of shapefiles at an 50 degree angle around the z-axis
    #td.rotate(data=shapefiles)
    #print('rotate_shapefiles -- done')

    # testing
    td.labels(data=decimated_meshes, coords=label_coordinates, names=label_names)
    print('testing -- done')

    # starts the app
    ui.colonia_4d()

