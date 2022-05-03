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

speedups.disable()


def shp_to_poly():
    # create geodataframes from all shapefiles
    polyDf = gpd.read_file('resources/shps/lakesPolygons.shp')

    # create emtpy dict to store the partial unstructure grids
    polyTubes = {}

    # iterate over the points
    for index, values in polyDf.iterrows():
        cellSec = []
        linePointSec = []

        # iterate over the geometry coords
        zipObject = zip(values.geometry.exterior.xy[0],
                        values.geometry.exterior.xy[1],
                        itertools.repeat(values.Elev))
        for linePoint in zipObject:
            linePointSec.append([linePoint[0], linePoint[1], linePoint[2]])

        # get the number of vertex from the line and create the cell sequence
        nPoints = len(list(polyDf.loc[index].geometry.exterior.coords))
        cellSec = [nPoints] + [i for i in range(nPoints)]

        # convert list to numpy arrays
        cellSecArray = np.array(cellSec)
        cellTypeArray = np.array([4])
        linePointArray = np.array(linePointSec)

        partialPolyUgrid = pv.UnstructuredGrid(cellSecArray, cellTypeArray, linePointArray)
        # we can add some values to the point
        partialPolyUgrid.cell_arrays["Elev"] = values.Elev
        polyTubes[str(index)] = partialPolyUgrid

    for idx, elem in enumerate(polyTubes.values()):
        elem.save(f'resources/vtks/shp_grid_{idx}.vtk', binary=False)


#shp_to_poly()

#print('Hello World')

#data = pv.read('../resources/vtks/shp_grid_2.vtk')

#poly_data = data.extract_surface()

#poly_data = poly_data.extrude([0, 0, 500])

#poly_data.plot()

