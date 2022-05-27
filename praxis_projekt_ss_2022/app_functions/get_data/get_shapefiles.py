# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import pyvista as pv
from app_functions.search_for_format import search_for_format


def do(sf_dict: dict, vtk_path: str):
    vtks = search_for_format(vtk_path, ['vtk'], cut=True)
    for elem in vtks:
        grid = pv.read(vtk_path + elem + '.vtk')
        grid_surface = grid.extract_surface()
        poly_data = pv.PolyData(grid_surface)
        sf_dict[elem] = poly_data
