import shutil
import pymeshlab
from app_functions.search_for_format import search_for_format

OBJ_PATH = 'models/shift_coords/obj_format/'
PLY_PATH = 'models/shift_coords/ply_format/'

ms = pymeshlab.MeshSet()


def obj_ply_convert():
    # list the current items in specific format
    obj_list = search_for_format(OBJ_PATH, ['obj'])
    ply_list = search_for_format(PLY_PATH, ['ply'])
    obj_rest_list = search_for_format(OBJ_PATH, ['jpg', 'mtl'])
    ply_rest_list = search_for_format(PLY_PATH, ['jpg', 'mtl'])

    # list every new item, that isnt already processed
    new_obj = [elem for elem in obj_list if elem not in ply_list]
    new_rest = [elem for elem in obj_rest_list if elem not in ply_rest_list]

    # copy all non .obj files
    for elem in new_rest:
        shutil.copyfile(OBJ_PATH + elem, PLY_PATH + elem)

    for elem in new_obj:
        print(elem)
        ms.load_new_mesh('models/shift_coords/obj_format/' + elem)
        ms.save_current_mesh('models/shift_coords/ply_format/' + elem[:elem.rfind('.')] + '.ply')
