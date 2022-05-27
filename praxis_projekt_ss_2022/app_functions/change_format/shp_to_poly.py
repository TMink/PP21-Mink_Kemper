# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import itertools
import numpy as np
import pyvista as pv
import geopandas as gpd

from shapely import speedups

from app_functions.search_for_format import search_for_format

speedups.disable()


def shp_to_poly(shp_path: str, vtk_path: str):
    # list the current items in specific format
    shp_list = search_for_format(shp_path, ['shp'], cut=True)
    vtk_list = search_for_format(vtk_path, ['vtk'], cut=True)

    for idx, elem in enumerate(vtk_list):
        if elem.rfind('_'):
            vtk_list[idx] = elem[:elem.rfind('_')]

    # list every new item, that isn't already processed
    new_shp = [elem for elem in shp_list if elem not in vtk_list]

    if new_shp:
        print('New Files:')
        for elem in new_shp:
            print(elem + "; ")
            # create geodataframes from all shapefiles
            geodataframes = gpd.read_file(shp_path + elem + '.shp')

            # create emtpy dict to store the partial unstructure grids
            unstructured_grids = {}

            # iterate over the points
            for index, values in geodataframes.iterrows():
                line_point_sec = []

                # iterate over the geometry coords
                zip_object = zip(values.geometry.exterior.xy[0],
                                values.geometry.exterior.xy[1],
                                itertools.repeat(values.Elev))
                for linePoint in zip_object:
                    line_point_sec.append([linePoint[0], linePoint[1], linePoint[2]])

                # get the number of vertex from the line and create the cell sequence
                n_points = len(list(geodataframes.loc[index].geometry.exterior.coords))
                cell_sec = [n_points] + [i for i in range(n_points)]

                # convert list to numpy arrays
                cell_sec_array = np.array(cell_sec)
                cell_type_array = np.array([4])
                line_point_array = np.array(line_point_sec)

                partial_poly_ugrid = pv.UnstructuredGrid(cell_sec_array, cell_type_array, line_point_array)
                # we can add some values to the point
                partial_poly_ugrid.cell_arrays["Elev"] = values.Elev
                unstructured_grids[str(index)] = partial_poly_ugrid

            for idx, value in enumerate(unstructured_grids.values()):
                value.save(f'resources/models/shapefiles/vtk/{elem}_{idx}.vtk', binary=False)
