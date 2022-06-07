# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Gets all .obj-files from ply_path and saves them temporarily into io_dict.
"""
# ---------------------------------------------------------------------------
import pyvista as pv
from app_functions.general.search_for_format import search_for_format


def do(io_dict: dict, ply_path: str):
    interaction_object = search_for_format(ply_path, ['ply'], cut=True)
    for elem in interaction_object:
        io = pv.read(ply_path + elem + '.ply')
        io.translate([-io.center[0], -io.center[1], -io.center[2]], inplace=True)
        io_dict[elem] = io
