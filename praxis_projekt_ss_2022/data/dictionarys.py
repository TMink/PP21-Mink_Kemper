# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import pyvista as pv


# To ensure the right types in the dictionary
class OriginalMeshes(dict):
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('key must be a str')
        if not isinstance(value, pv.PolyData):
            raise ValueError('value must be a polydata object')
        dict.__setitem__(self, key, value)


# original_layers_name(str) : original_layers.ply(PolyData)
# layers of the excavation side, before they are decimated
original_layers = OriginalMeshes()

# decimated_layer_name(str) : decimated_layer.ply(PolyDat)
# layers of the excavation side, which are already decimated
#decimated_layers = DecimatedMeshes()

# excavation_layers_name(str) : excavation_layers_plotted(VTK)
# plotted layers of the excavation side
excavation_layers = {}

# segmentation_extraction_layers_name(str) : segmentation_extraction_layers(VTK)
# clipped and plotted layers of the segmentation/extraction tool
segmentation_extraction_layers = {}

# segmentation_tool: clipped_layer_name : clipped_layers_seg_ex.ply(PolyData)
# extraction_tool: clipped_layer_name : clipped_layers_seg_ex.ply(UnstructuredGrid)
# clipped layers, used from segemntation_tool/extraction_tool. Type depends of tool
segmentation_extraction_clipped_layers = {}




'''
************************************************************************************************************************
***                                                    Shapefiles                                                    ***
************************************************************************************************************************
'''
# shapefiles_name(str) : shapefiles.ply(PolyData)
# shape files
shapefiles = {}

# shapefiles_layers_name : shypefiles_layers(VTK)
# plotted shapefiles
shapefiles_layers = {}

# checkbox_name : checkbox'
# clipped and plotted shapefiles
shapefiles_clipped_layers = {}

all_subdivided_layers = {}

shapefiles_clipped_and_subdivided_layers = {}

# shapefiles_name(str) : color(str)
# shape files
shapefiles_colors = {}

# shapefiles_name(str) : color(str)
# shape files
shapefiles_colors_actual = {}

# shapefiles_name(str) : color(str)
# shape files
shapefiles_checkboxes = {}

# shapefiles_name(str) : color(str)
# shape files
shapefiles_selected_for_clipping = {}



'''
************************************************************************************************************************
***                                              Interaction Object                                                  ***
************************************************************************************************************************
'''
# interactable_objects_name(str) : interactable_objects.ply(PolyData)
# interactable objects
interaction_objects = {}

# interactable_objects_name(str) : interactable_objects.ply(PolyData)
# interactable objects, which are in the scene and not yet plotted
interaction_objects_loaded = {}

# interactable_objects_name : interactable_objects(VTK)
# plotted interactable objects
interaction_objects_plotted = {}

# found_name(str) : found_plotted(VTK)
# founds
founds = {}

# checkbox_name(str) : found_name(str)
# corresponding names of checkbox and found
founds_checkboxes = {}

# checkbox_name : checkbox
# check box
check_boxes = {}

# dummy_layer_name(str) : decimated_layer(VTK)
# first layer of decimated_layers
dummy_layer = {}

# interactable_objects_name(str) : QPushButton
# button of existing interactable objects, that could be loaded in the scene
buttons_not_in_plot = {}

# interactable_objects_name(str) : QPushButton
# button of interactable objects, that are loaded in the scene
buttons_in_plot = {}

geotiff_bounds = {}

old_utm_coords = {}
