import shutil
import pymeshlab
from app_functions.search_for_format import search_for_format

OBJ_PATH = 'models/shift_coords/obj_format/'
PLY_PATH = 'models/shift_coords/ply_format/'

ms = pymeshlab.MeshSet()


def obj_ply_convert():
    obj_list = search_for_format(OBJ_PATH, ['obj'])
    rest_list = search_for_format(OBJ_PATH, ['jpg', 'mtl'])

    print(obj_list)
    print(rest_list)

    # copy all non .obj files
    for elem in rest_list:
        shutil.copyfile(OBJ_PATH + elem, PLY_PATH + elem)

    for elem in obj_list:
        print(elem)
        ms.load_new_mesh('models/shift_coords/obj_format/' + elem)
        ms.save_current_mesh('models/shift_coords/ply_format/' + elem[:elem.rfind('.')] + '.ply')
