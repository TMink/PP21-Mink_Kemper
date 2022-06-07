# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Gets all .jpg-files from jpg_path and saves them temporarily into t_list.
"""
# ---------------------------------------------------------------------------
import pyvista as pv
from app_functions.general.search_for_format import search_for_format


def do(t_list: list, jpg_path: str):
    textures = search_for_format(jpg_path, ['jpg'], cut=False)
    for elem in textures:
        t_list.append(pv.read_texture(jpg_path + elem))
