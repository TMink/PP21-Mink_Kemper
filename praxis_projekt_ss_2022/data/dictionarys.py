# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Temporary data.
"""
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


# original_layers_name(str) : original_layers(PolyData)
# layers of the excavation side, before they are decimated
original_layers = OriginalMeshes()

# decimated_layer_name(str) : decimated_layer(PolyDat)
# layers of the excavation side, which are already decimated
# decimated_layers = DecimatedMeshes()

# excavation_layers_name(str) : excavation_layers_plotted(VisualisationToolkit)
# plotted layers of the excavation side
excavation_layers = {}

# segmentation_extraction_layers_name(str) : segmentation_extraction_layers(VisualisationToolkit)
# clipped and plotted layers of the segmentation/extraction tool
segmentation_extraction_layers = {}

# segmentation_tool: clipped_layer_name(str) : clipped_layers_seg_ex(PolyData)
# extraction_tool: clipped_layer_name(str) : clipped_layers_seg_ex(UnstructuredGrid)
# clipped layers, used from segmentation_tool/extraction_tool. Type depends on tool
segmentation_extraction_clipped_layers = {}




'''
************************************************************************************************************************
***                                                    Shapefiles                                                    ***
************************************************************************************************************************
'''
# shapefiles_name(str) : shapefiles(PolyData)
# shapefiles
shapefiles = {}

# shapefiles_layers_name(str) : shypefiles_layers(VisualisationToolkit)
# plotted shapefiles
shapefiles_layers = {}

# shapefile_name_idx(str) : shapefiles_clipped_layers(PolyData)
# every selected element (invert cut)
shapefiles_clipped_layers = {}

# all_subdivided_layers_name : all_subdivided_layers(PolyData)
# every original_layer (normal cut)
all_subdivided_layers = {}

# shapefile_name_idx : shapefiles_clipped_layers(VisualisationToolkit)
# and
# all_subdivided_layers_name : all_subdivided_layers(VisualisationToolkit)
# plotted invert- and normal cuts
shapefiles_clipped_and_subdivided_layers = {}

# shapefiles_name(str) : color(str)
# shapefile colors if selected
shapefiles_colors = {}

# shapefiles_name(str) : color(str)
# shapefile actual colors at the time
shapefiles_colors_actual = {}

# shapefiles_name(str) : QCheckBox
shapefiles_checkboxes = {}

# shapefiles_checkboxes_name(str) : shapefiles[shapefiles_checkboxes_name](PolyData)
shapefiles_selected_for_clipping = {}




'''
************************************************************************************************************************
***                                              Interaction Object                                                  ***
************************************************************************************************************************
'''
# interaction_objects_name(str) : interaction_objects.ply(PolyData)
# interaction objects
interaction_objects = {}

# interaction_objects_name(str) : interaction_objects.ply(PolyData)
# interaction objects, which are in the scene and not yet plotted
interaction_objects_loaded = {}

# interactable_objects_name(str) : interactable_objects(VTK)
# plotted interactable objects
interaction_objects_plotted = {}

# interactable_objects_name(str) : QPushButton
# button of existing interactable objects, that could be loaded in the scene
buttons_not_in_plot = {}

# interactable_objects_name(str) : QPushButton
# button of interactable objects, that are loaded in the scene
buttons_in_plot = {}


'''
************************************************************************************************************************
***                                                      Founds                                                      ***
************************************************************************************************************************
'''
# found_name(str) : found_plotted(VTK)
# founds
founds = {}

# checkbox_name(str) : found_name(str)
# corresponding names of checkbox and found
founds_checkboxes = {}

# checkbox_name : checkbox
# check box
check_boxes = {}




'''
************************************************************************************************************************
***                                                  Dummy Layer                                                     ***
************************************************************************************************************************
'''
# dummy_layer_name(str) : decimated_layer(VTK)
# first layer of decimated_layers
dummy_layer = {}




'''
************************************************************************************************************************
***                                                    GeoTIFF                                                       ***
************************************************************************************************************************
'''
# perspective_name(str) : cords(Int)
# cords used by the raster-algorithm of gdal
geotiff_bounds = {}

# 'geotiff': geotiff_name(str)
# last created geotiff
geotiff_new = {}
