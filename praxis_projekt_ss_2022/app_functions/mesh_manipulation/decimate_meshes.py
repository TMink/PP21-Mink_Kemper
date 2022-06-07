# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Gets all -ply-files from ply_path, decimates the given meshes into a TARGET-vertex-size and saves the new .ply-files in
decimated_ply_path

-1- Get all files (.ply, .jpg, .mtl) from ply_path and decimated_ply_path
-2- Looks if files are already present in decimated_ply_path
-3- Copy all non .ply files into decimated_ply_path
-4- Decimates all meshes and saves them
"""
# ---------------------------------------------------------------------------
import shutil
import pymeshlab as ml

from app_functions.general.search_for_format import search_for_format

# Maximum triangles of the decimated mesh
TARGET = 100000

ms = ml.MeshSet()


def do(ply_path: str, decimated_ply_path: str):
    # -1-
    ply_list = search_for_format(ply_path, ['ply'], cut=False)
    decimated_ply_list = search_for_format(decimated_ply_path, ['ply'], cut=False)
    ply_rest_list = search_for_format(ply_path, ['mtl', 'jpg'], cut=False)
    decimated_ply_rest_list = search_for_format(decimated_ply_path, ['mtl', 'jpg'], cut=False)

    # -2-
    new_ply_list = [elem for elem in ply_list if elem not in decimated_ply_list]
    new_rest_list = [elem for elem in ply_rest_list if elem not in decimated_ply_rest_list]

    # -3-
    for elem in new_rest_list:
        try:
            shutil.copyfile(ply_path + elem, decimated_ply_path + elem)
        except OSError:
            print(f'cannot copy {elem} from {ply_path} to {decimated_ply_path}')

    # -4-
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
