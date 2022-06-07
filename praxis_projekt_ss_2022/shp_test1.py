#import required packages
import itertools
import numpy as np
import pyvista as pv
import geopandas as gpd
#for windows users
from shapely import speedups
speedups.disable()

SHP_PATH = 'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/shapefiles/shp/'
VTK_PATH = 'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/shapefiles/vtk/lakePolyasLines.vtk'

#create geodataframes from all shapefiles
#pointDf = gpd.read_file('../Shps/wellPoints.shp')
#lineDf = gpd.read_file('../Shps/contoursLines.shp')
polyDf = gpd.read_file(SHP_PATH)

#create emtpy dict to store the partial unstructure grids
polyTubes = {}

#iterate over the points
for index, values in polyDf.iterrows():
    cellSec = []
    linePointSec = []

    # iterate over the geometry coords
    zipObject = zip(values.geometry.exterior.xy[0],
                    values.geometry.exterior.xy[1],
                    itertools.repeat(values.Elev))

    print(f'{values.geometry.exterior.xy[0][0]}, {values.geometry.exterior.xy[1][0]}')



    for linePoint in zipObject:
        linePointSec.append([linePoint[0],linePoint[1],linePoint[2]])
        print([linePoint[0], linePoint[1], linePoint[2]])

    #get the number of vertex from the line and create the cell sequence
    nPoints = len(list(polyDf.loc[index].geometry.exterior.coords))
    cellSec = [nPoints] + [i for i in range(nPoints)]

    #convert list to numpy arrays
    cellSecArray = np.array(cellSec)
    cellTypeArray = np.array([4])
    linePointArray = np.array(linePointSec)

    partialPolyUgrid = pv.UnstructuredGrid(cellSecArray,cellTypeArray,linePointArray)
    #we can add some values to the point
    partialPolyUgrid.cell_arrays["Elev"] = values.Elev
    #    partialPolyUgrid.save('../vtk/partiallakePoly.vtk',binary=False)
    polyTubes[str(index)] = partialPolyUgrid

#merge all tubes and export resulting vtk
polyBlocks = pv.MultiBlock(polyTubes)
polyGrid = polyBlocks.combine()
polyGrid.save(VTK_PATH, binary=False)
polyGrid.plot()
