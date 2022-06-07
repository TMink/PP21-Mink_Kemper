import geopandas as gpd
from dbfread import DBF
import shapefile
import pyvista as pv

from app_functions.general.search_for_format import search_for_format

#SHP_PATH = 'resources/models/shapefiles/shp/'

#shp_list = search_for_format(SHP_PATH, ['shp'], cut=False)
#dbf_list = search_for_format(SHP_PATH, ['shp'], cut=False)

#shape = gpd.read_file(SHP_PATH + shp_list[0])
#print(shape)

#dbfReader = shapefile.Reader(dbf=SHP_PATH + dbf_list[0])
#list = dbfReader.records()
#for elem in list:
#    print(elem)

VTK_PATH = 'C:/Users/Tobias/Desktop/Praxisprojekt SS2022/New/PP21-Mink_Kemper/praxis_projekt_ss_2022/resources/models/shapefiles/vtk/'

shapefiles_polydata_dict = {}

plotter = pv.Plotter()

# get all shapefiles as vtk and transform them to polydata
vtks = search_for_format(VTK_PATH, ['vtk'], cut=True)
for elem in vtks:
    grid = pv.read(VTK_PATH + elem + '.vtk')
    grid_surface = grid.extract_surface()
    shapefiles_polydata_dict[elem] = grid_surface
print('----collected all vtks----')

#for key, value in shapefiles_polydata_dict.items():
#    plotter.add_mesh(mesh=value, name=key)

plotter.add_mesh(mesh=list(shapefiles_polydata_dict.values())[2], name=list(shapefiles_polydata_dict.keys())[2])

plotter.show()
