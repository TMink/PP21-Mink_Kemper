# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import shutil
from app_functions.search_for_format import search_for_format
import pymeshlab as ml

PLY_PATH = 'resources/models/shift_coords/ply_format/'
DECIMATED_PLY_PATH = 'resources/models/shift_coords/ply_format/decimated/'

# Maximum triangles of the decimated mesh
TARGET = 100000

ms = ml.MeshSet()


def decimate_meshes():
    ply_list = search_for_format(PLY_PATH, ['ply'], cut=False)
    decimated_ply_list = search_for_format(DECIMATED_PLY_PATH, ['ply'], cut=False)
    ply_rest_list = search_for_format(PLY_PATH, ['mtl', 'jpg'], cut=False)
    decimated_ply_rest_list = search_for_format(DECIMATED_PLY_PATH, ['mtl', 'jpg'], cut=False)

    new_ply_list = [elem for elem in ply_list if elem not in decimated_ply_list]
    new_rest_list = [elem for elem in ply_rest_list if elem not in decimated_ply_rest_list]

    # copy all non .ply files
    for elem in new_rest_list:
        try:
            shutil.copyfile(PLY_PATH + elem, DECIMATED_PLY_PATH + elem)
        except OSError:
            print(f'cannot copy {elem} from {PLY_PATH} to {DECIMATED_PLY_PATH}')

    for elem in new_ply_list:
        ms.load_new_mesh(PLY_PATH + elem)
        num_faces = 100 + 2 * TARGET

        # Simplify
        while ms.current_mesh().vertex_number() > TARGET:
            ms.apply_filter('simplification_quadric_edge_collapse_decimation', targetfacenum=num_faces,
                            preservenormal=True)
            # Refine our estimation to slowly converge to TARGET vertex number
            num_faces = num_faces - (ms.current_mesh().vertex_number() - TARGET)

        ms.save_current_mesh(DECIMATED_PLY_PATH + elem)
