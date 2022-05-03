# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

import pyvista as pv


# To ensure the right types in the dictionary
class DecimatedMeshes(dict):
    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('key must be a str')
        if not isinstance(value, pv.PolyData):
            raise ValueError('value must be a polydata object')
        dict.__setitem__(self, key, value)


# dict with 'label_name : plotted_label' ( str : VTK )
# example -> 'label_name : self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key], point_size=20,
#                                                     font_size=36, name='label_name', reset_camera=False)
decimated_meshes = DecimatedMeshes()

# dict with 'layer_name : plotted layer' ( str : VTK )
# example -> 'layer_name' : self.plotter.add_mesh(mesh=decimated_mesh[0], name='layer_name', texture=textures[0])
excavation_layers = {}

# dict with 'clipped_layer_name : plotted_clipped_layer' ( str : VTK )
# example -> 'clipped_layer_name' : self.plotter.add_mesh(mesh=clipped_meshes[0], texture=textures[0],
#                                                      name='clipped_layer_name', show_scalar_bar=False,
#                                                      reset_camera=False)
# If used in segmentation tool: plotted_clipped_layer == PolyData
# If used in extraction tool  : plotted_clipped_layer == UnstructuredGrid
clipped_layers_seg_ex = {}

# dict with 'label_name : plotted_label' ( str : VTK )
# example -> 'label_name : self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key], point_size=20,
#                                                     font_size=36, name='label_name', reset_camera=False)
labels = {}

# dict with 'object_name : plotted object' ( str : VTK )
# example ->
interaction_objects = {}

# dict with 'checkbox_name : label_name' ( str :  )
# example -> 'label_name : self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key], point_size=20,
#
labels_checkboxes = {}

# dict with 'checkbox_name : checkbox' ( str :  )
# example -> 'label_name : self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key], point_size=20,
#
check_boxes = {}

# dict with 'checkbox_name : checkbox' ( str :  )
# example -> 'label_name : self.plotter.add_point_labels(points=[visible_labels[key]], labels=[key], point_size=20,
#
clipped_layers_shp = {}
