# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import re

from matplotlib import colors as mcolors

import pyvista as pv
from app_functions.general.search_for_format import search_for_format


def do(sf_dict: dict, sf_c_dict: dict, sf_c_a_dict: dict, vtk_path: str):

    vtks = search_for_format(vtk_path, ['vtk'], cut=True)
    vtk_names = []
    vtk_polydata = {}

    next_shapefile = ''
    which_color = -1

    colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)

    # Sort colors by hue, saturation, value and name.
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                    for name, color in colors.items())
    sorted_names = [name for hsv, name in by_hsv]

    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [atoi(c) for c in re.split(r'(\d+)', text)]

    for elem in vtks:
        vtk_names.append(elem)
        grid = pv.read(vtk_path + elem + '.vtk')
        grid_surface = grid.extract_surface()
        vtk_polydata[elem] = grid_surface

    vtk_names.sort(key=natural_keys)

    print('just testing')

    for elem in vtk_names:
        sf_dict[elem] = vtk_polydata[elem]
        sf_c_a_dict[elem] = 'white'

        name = elem[:elem.rfind('_')]
        if name != next_shapefile:
            next_shapefile = name
            which_color += 1
        sf_c_dict[name] = sorted_names[which_color]

