# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import shutil
import pymeshlab
from app_functions.search_for_format import search_for_format

ms = pymeshlab.MeshSet()


def do(obj_path: str, ply_path: str):
    # list the current items in specific format
    obj_list = search_for_format(obj_path, ['obj'], cut=True)
    ply_list = search_for_format(ply_path, ['ply'], cut=True)
    obj_rest_list = search_for_format(obj_path, ['jpg', 'mtl'], cut=False)
    ply_rest_list = search_for_format(ply_path, ['jpg', 'mtl'], cut=False)

    # list every new item, that isn't already processed
    new_obj = [elem for elem in obj_list if elem not in ply_list]
    new_rest = [elem for elem in obj_rest_list if elem not in ply_rest_list]

    # copy all .obj files
    if new_obj:
        print('New files:')
        for elem in new_obj:
            print(elem)
            ms.load_new_mesh(obj_path + elem + '.obj')
            ms.save_current_mesh(ply_path + elem + '.ply')

    # copy all non .obj files
    for elem in new_rest:
        try:
            shutil.copyfile(obj_path + elem, ply_path + elem)
        except OSError:
            print(f'cannot copy {elem} from {obj_path} to {ply_path}')


