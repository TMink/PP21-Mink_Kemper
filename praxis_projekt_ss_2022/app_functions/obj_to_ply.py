# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import shutil
import pymeshlab
from app_functions.search_for_format import search_for_format

OBJ_PATH = 'resources/models/shift_coords/obj_format/'
PLY_PATH = 'resources/models/shift_coords/ply_format/'

ms = pymeshlab.MeshSet()


def oby_to_ply():
    # list the current items in specific format
    obj_list = search_for_format(OBJ_PATH, ['obj'], cut=True)
    ply_list = search_for_format(PLY_PATH, ['ply'], cut=True)
    obj_rest_list = search_for_format(OBJ_PATH, ['jpg', 'mtl'], cut=False)
    ply_rest_list = search_for_format(PLY_PATH, ['jpg', 'mtl'], cut=False)

    # list every new item, that isnt already processed
    new_obj = [elem for elem in obj_list if elem not in ply_list]
    new_rest = [elem for elem in obj_rest_list if elem not in ply_rest_list]

    if new_obj:
        print('New files:')

    # copy all non .obj files
    for elem in new_rest:
        shutil.copyfile(OBJ_PATH + elem, PLY_PATH + elem)

    for elem in new_obj:
        print(elem)
        ms.load_new_mesh(OBJ_PATH + elem + '.obj')
        ms.save_current_mesh(PLY_PATH + elem + '.ply')
