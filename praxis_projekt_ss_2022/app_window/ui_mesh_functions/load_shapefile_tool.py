# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Loads every polygon from shapefiles into the plot.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import excavation_layers, segmentation_extraction_clipped_layers, \
    segmentation_extraction_layers, shapefiles_layers, shapefiles, shapefiles_clipped_and_subdivided_layers, \
    shapefiles_selected_for_clipping, shapefiles_colors_actual, shapefiles_checkboxes, founds


def do(self, state=None):
    if state:
        self.plotter.remove_bounds_axes()
        # clear and reset
        self.plotter.remove_actor(excavation_layers.keys())
        self.plotter.remove_actor(segmentation_extraction_clipped_layers.keys())
        self.plotter.remove_actor(segmentation_extraction_layers.keys())
        self.plotter.remove_actor(shapefiles_layers.keys())
        self.plotter.remove_actor(shapefiles_clipped_and_subdivided_layers.keys())
        self.plotter.remove_actor(founds.keys())

        self.plotter.clear_plane_widgets()
        self.plotter.clear_box_widgets()

        self.excavation_side_texture.setChecked(False)
        self.excavation_side_color.setChecked(False)
        self.segmentation_tool_texture.setChecked(False)
        self.segmentation_tool_color.setChecked(False)
        self.extraction_tool_texture.setChecked(False)
        self.extraction_tool_color.setChecked(False)
        self.founds_show_hide.setChecked(False)

        excavation_layers.clear()
        segmentation_extraction_clipped_layers.clear()
        segmentation_extraction_layers.clear()
        shapefiles_layers.clear()
        shapefiles_clipped_and_subdivided_layers.clear()
        shapefiles_selected_for_clipping.clear()

        self.interaction_objects_label.hide()
        self.interaction_accessible_objects_scroll_area.hide()
        self.interaction_loaded_objects_scroll_area.hide()
        self.interaction_objects_create_button.hide()
        self.interaction_objects_delete_button.hide()
        self.interaction_objects_object_view_mode_button.hide()
        self.interaction_objects_info_panel.setChecked(False)

        self.found_label.hide()
        self.found_scroll_area.hide()
        self.founds_info_panel.setChecked(False)

        for elem in shapefiles_colors_actual.keys():
            shapefiles_colors_actual[elem] = 'white'

        for name, polygon in shapefiles.items():
            shapefiles_layers[name] = self.plotter.add_mesh(mesh=polygon, name=name)

    else:
        self.shapefile_tool_load.setChecked(False)

        self.plotter.remove_actor(shapefiles_layers.keys())
        self.plotter.remove_actor(shapefiles_clipped_and_subdivided_layers.keys())

        shapefiles_layers.clear()
        shapefiles_clipped_and_subdivided_layers.clear()

        self.shapefile_tool_load_button.hide()
        self.shapefile_tool_scroll_area.hide()
        self.shapefile_tool_info_panel.setChecked(False)

