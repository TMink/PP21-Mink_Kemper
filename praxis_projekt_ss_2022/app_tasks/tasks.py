# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import time

from app_functions.change_format import obj_to_ply, shp_to_poly, utm_to_shift
from app_functions.get_data import get_founds, get_interaction_objects, get_meshes, get_shapefiles, get_textures
from app_functions.mesh_manipulation import decimate_meshes, translate_interaction_objects
import app_window.pyvista_ui as ui

from data.dictionarys import *
from data.lists import *

UTM_PATH = 'resources/models/excavation_layers/layers_utm/'
OBJ_PATH = 'resources/models/excavation_layers/layers_shift/obj/'
PLY_PATH = 'resources/models/excavation_layers/layers_shift/ply/'
JPG_PATH = 'resources/models/excavation_layers/layers_shift/ply/decimated_layers/'
DECIMATED_PLY_PATH = 'resources/models/excavation_layers/layers_shift/ply/decimated_layers/'

OBJECT_OBJ_PATH = 'resources/models/interactable_objects/obj/'
OBJECT_PLY_PATH = 'resources/models/interactable_objects/ply/'

SHP_PATH = 'resources/models/shapefiles/shp/'
VTK_PATH = 'resources/models/shapefiles/vtk/'

tasks = {}
task = lambda t: tasks.setdefault(t.__name__, t)


@task
def layers___utm_to_shift():
    utm_to_shift.do(utm_path=UTM_PATH, shift_path=OBJ_PATH)


@task
def layers___object_to_ply():
    obj_to_ply.do(obj_path=OBJ_PATH, ply_path=PLY_PATH)


@task
def layers___decimate_meshes():
    decimate_meshes.do(ply_path=PLY_PATH, decimated_ply_path=DECIMATED_PLY_PATH)


@task
def layers_origional___get_meshes():
    get_meshes.do(dict=original_layers, ply_path=PLY_PATH)


@task
def layers_decimated___get_meshes():
    get_meshes.do(dict=decimated_layers, ply_path=DECIMATED_PLY_PATH)


@task
def layers___get_textures():
    get_textures.do(t_list=textures, jpg_path=JPG_PATH)


@task
def interaction_objects___obj_to_ply():
    obj_to_ply.do(obj_path=OBJECT_OBJ_PATH, ply_path=OBJECT_PLY_PATH)


@task
def interaction_objects___get_interaction_objects():
    get_interaction_objects.do(io_dict=interactable_objects, ply_path=OBJECT_PLY_PATH)


@task
def shapefiles___get_shapefiles():
    get_shapefiles.do(sf_dict=shapefiles, vtk_path=VTK_PATH)


@task
def interaction_objects___translate_interaction_objects():
    translate_interaction_objects.do(data=interactable_objects.values())


@task
def founds___get_founds():
    get_founds.do(data=decimated_layers, coords=found_coordinates, names=found_names)


@task
def start():
    ui.colonia_4d()


def compute():
    without_start = [func_name for func_name in tasks.keys()]
    without_start = without_start[:-1]
    for key in without_start:
        tasks[key]()
        time.sleep(0.2)
        yield


def task_quantity():
    return len(tasks) - 1
