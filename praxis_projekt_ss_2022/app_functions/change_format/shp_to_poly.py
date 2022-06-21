# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Converts every new shp files into PolyData-Objects
"""
# ---------------------------------------------------------------------------
import shutil

import numpy as np
import geopandas as gpd

from shapely import speedups

from app_functions.general.search_for_format import search_for_format

import pyvista as pv

speedups.disable()

SHP_PATH = \
    'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/' \
    'shapefiles/shp/'
VTK_PATH = \
    'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/' \
    'shapefiles/vtk/'

PLY_PATH = \
    'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/' \
    'excavation_layers/layers_shift/ply/'
JPG_PATH = \
    'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/' \
    'excavation_layers/layers_shift/ply/decimated_layers/'

SUB_PATH = \
    'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/' \
    'subdivided_meshes/'


def do(shp_path: str, vtk_path: str):
    # Get all files (.shp, .cpg, .dbf, .prj, .sbn, .sbx, .shx, .sr) from shp_path and vtk_path
    shp_list = search_for_format(path=shp_path, format_type=['shp'], cut=True, exceptions=['sr', 'xml'])
    shp_rest_list = search_for_format(path=shp_path,
                                      format_type=['cpg', 'dbf', 'prj', 'sbn', 'sbx', 'shx', 'sr'], cut=False)
    vtk_list = search_for_format(path=vtk_path, format_type=['vtk'], cut=True)
    vtk_rest_list = search_for_format(path=vtk_path,
                                      format_type=['cpg', 'dbf', 'prj', 'sbn', 'sbx', 'shx', 'sr'], cut=False)

    # cut the index of every vtk for comparison
    for idx, elem in enumerate(vtk_list):
        if elem.rfind('_'):
            vtk_list[idx] = elem[:elem.rfind('_')]

    # Looks if files are already present in vtk_path
    new_shp = [elem for elem in shp_list if elem not in vtk_list]
    new_rest = [elem for elem in shp_rest_list if elem not in vtk_rest_list]

    # Copy all non .obj files into ply_path
    for elem in new_rest:
        try:
            shutil.copyfile(shp_path + elem, vtk_path + elem)
        except OSError:
            print(f'cannot copy {elem} from {shp_path} to {vtk_path}')

    # Convert .shp-files into .vtk-files, shift the cords, attach an index value polygons and save those polygons into
    # vtk_path
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
                                 values.geometry.exterior.xy[1])

                for linePoint in zip_object:
                    new_x = round(((float(linePoint[0]) / 100) - int(float(linePoint[0]) / 100)) * 100, 6)
                    new_y = round(((float(linePoint[1]) / 100) - int(float(linePoint[1]) / 100)) * 100, 6)
                    print(f'new_x: {new_x}, new_y: {new_y}')
                    # line_point_sec.append([linePoint[0], linePoint[1], 100])
                    line_point_sec.append([new_x, new_y, 15])

                # get the number of vertex from the line and create the cell sequence
                n_points = len(list(geodataframes.loc[index].geometry.exterior.coords))
                cell_sec = [n_points] + [i for i in range(n_points)]

                # convert list to numpy arrays
                cell_sec_array = np.array(cell_sec)
                cell_type_array = np.array([4])
                line_point_array = np.array(line_point_sec)

                partial_poly_ugrid = pv.UnstructuredGrid(cell_sec_array, cell_type_array, line_point_array)
                unstructured_grids[str(index)] = partial_poly_ugrid

            # save the polygon with index as vtk
            for idx, value in enumerate(unstructured_grids.values()):
                value.save(VTK_PATH + f'{elem}_{idx}.vtk', binary=False)
