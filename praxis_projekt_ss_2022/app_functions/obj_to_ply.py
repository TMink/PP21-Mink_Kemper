import pymeshlab
from app_functions.search_for_format import search_for_obj

ms = pymeshlab.MeshSet()


def obj_ply_convert():
    obj_list = search_for_obj('../models/shift_coords/obj_format/schnitt_17_07')
    for elem in obj_list:
        print(elem)
        ms.load_new_mesh('../models/shift_coords/schnitt_17_07/' + elem)
        ms.save_current_mesh('../models/shift_coords/ply_format/schnitt_17_07/' + elem[:elem.rfind('.')] + '.ply')


obj_ply_convert()
