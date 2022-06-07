# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import pyvista as pv
from app_functions.general.search_for_format import search_for_format


def do(mesh_dict: dict, ply_path: str):
    meshes = search_for_format(ply_path, ['ply'], cut=False)
    for elem in meshes:
        layer_data = elem.split(' ')
        mesh_dict[layer_data[0]] = pv.read(ply_path + elem)
