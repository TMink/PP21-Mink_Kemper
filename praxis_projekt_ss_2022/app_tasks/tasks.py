# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import time

from app_functions.change_format import obj_to_ply, utm_to_shift
from app_functions.get_data import get_founds, get_interaction_objects, get_meshes, get_textures, get_shapefiles
from app_functions.mesh_manipulation import translate_interaction_objects
import app_window.pyvista_ui as ui

from data.dictionarys import original_layers, interaction_objects, shapefiles, shapefiles_colors, \
    shapefiles_colors_actual
from data.lists import textures, found_coordinates, found_names

UTM_PATH = 'resources/models/excavation_layers/layers_utm/'
OBJ_PATH = 'resources/models/excavation_layers/layers_shift/obj/'
PLY_PATH = 'resources/models/excavation_layers/layers_shift/ply/'
JPG_PATH = 'resources/models/excavation_layers/layers_shift/ply/decimated_layers/'
DECIMATED_PLY_PATH = 'resources/models/excavation_layers/layers_shift/ply/decimated_layers/'

OBJECT_OBJ_PATH = 'resources/models/interaction_objects/obj/'
OBJECT_PLY_PATH = 'resources/models/interaction_objects/ply/'

SHP_PATH = 'resources/models/shapefiles/shp/'
VTK_PATH = 'resources/models/shapefiles/vtk/'

tasks_names = [
    'Changing utm- to shift-coordinates',
    'Changing layer format from ".obj" to ".ply"',
    'Load original meshes',
    'Load textures',
    'Changing interaction object format from ".obj" to ".ply"',
    'Load interaction objects',
    'Load shapefiles',
    'Translate interaction objects',
    'Load founds'
]

tasks = {}
task = lambda t: tasks.setdefault(t.__name__, t)


@task
def layers___utm_to_shift():
    utm_to_shift.do(utm_path=UTM_PATH, shift_path=OBJ_PATH)


@task
def layers___object_to_ply():
    obj_to_ply.do(obj_path=OBJ_PATH, ply_path=PLY_PATH)


#@task
#def layers___decimate_meshes():
#    decimate_meshes.do(ply_path=PLY_PATH, decimated_ply_path=DECIMATED_PLY_PATH)


@task
def layers_origional___get_meshes():
    get_meshes.do(mesh_dict=original_layers, ply_path=PLY_PATH)


#@task
#def layers_decimated___get_meshes():
#    get_meshes.do(dict=decimated_layers, ply_path=DECIMATED_PLY_PATH)


@task
def layers___get_textures():
    get_textures.do(t_list=textures, jpg_path=JPG_PATH)


@task
def interaction_objects___obj_to_ply():
    obj_to_ply.do(obj_path=OBJECT_OBJ_PATH, ply_path=OBJECT_PLY_PATH)


@task
def interaction_objects___get_interaction_objects():
    get_interaction_objects.do(io_dict=interaction_objects, ply_path=OBJECT_PLY_PATH)


#@task
#def shapefiles___shp_to_poly():
#    shp_to_poly.do(shp_path=SHP_PATH, vtk_path=VTK_PATH)
#    print('Finished')


@task
def shapefiles___get_shapefiles():
    get_shapefiles.do(sf_dict=shapefiles, sf_c_dict=shapefiles_colors, sf_c_a_dict=shapefiles_colors_actual, vtk_path=VTK_PATH)


@task
def interaction_objects___translate_interaction_objects():
    translate_interaction_objects.do(data=interaction_objects.values())


@task
def founds___get_founds():
    get_founds.do(data=original_layers, cords=found_coordinates, names=found_names)
    print(f'erster Versuch: {len(found_coordinates)}')


@task
def start():
    ui.colonia_4d()
