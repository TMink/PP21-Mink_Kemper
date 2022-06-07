# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import shutil
import pymeshlab as ml

from app_functions.general.search_for_format import search_for_format

# Maximum triangles of the decimated mesh
TARGET = 100000

ms = ml.MeshSet()


# takes the original mesh and decimates it a to a smaller size (performance)
def do(ply_path: str, decimated_ply_path: str):
    ply_list = search_for_format(ply_path, ['ply'], cut=False)
    decimated_ply_list = search_for_format(decimated_ply_path, ['ply'], cut=False)
    ply_rest_list = search_for_format(ply_path, ['mtl', 'jpg'], cut=False)
    decimated_ply_rest_list = search_for_format(decimated_ply_path, ['mtl', 'jpg'], cut=False)

    new_ply_list = [elem for elem in ply_list if elem not in decimated_ply_list]
    new_rest_list = [elem for elem in ply_rest_list if elem not in decimated_ply_rest_list]

    # copy all non .ply files
    for elem in new_rest_list:
        try:
            shutil.copyfile(ply_path + elem, decimated_ply_path + elem)
        except OSError:
            print(f'cannot copy {elem} from {ply_path} to {decimated_ply_path}')

    for elem in new_ply_list:
        ms.load_new_mesh(ply_path + elem)
        num_faces = 100 + 2 * TARGET

        # Simplify
        while ms.current_mesh().vertex_number() > TARGET:
            ms.apply_filter('simplification_quadric_edge_collapse_decimation', targetfacenum=num_faces,
                            preservenormal=True)
            # Refine our estimation to slowly converge to TARGET vertex number
            num_faces = num_faces - (ms.current_mesh().vertex_number() - TARGET)

        ms.save_current_mesh(decimated_ply_path + elem)
