# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Loads every mesh from original_layers into the plot.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import dummy_layer, excavation_layers, segmentation_extraction_clipped_layers, \
    segmentation_extraction_layers, shapefiles_layers, original_layers, shapefiles_clipped_and_subdivided_layers
from data.lists import dummy_semaphore, excavation_semaphor, textures, colors


def do(self, state=None):
    # In case the user switches between tools and do not uncheck them, the semaphore get reset
    dummy_semaphore[0] = 1
    dummy_layer.clear()

    self.plotter.show_grid()

    # clear and reset
    self.plotter.remove_actor(excavation_layers.keys())
    self.plotter.remove_actor(segmentation_extraction_clipped_layers.keys())
    self.plotter.remove_actor(segmentation_extraction_layers.keys())
    self.plotter.remove_actor(shapefiles_layers.keys())
    self.plotter.remove_actor(shapefiles_clipped_and_subdivided_layers.keys())

    self.plotter.clear_plane_widgets()
    self.plotter.clear_box_widgets()

    self.segmentation_tool_texture.setChecked(False)
    self.segmentation_tool_color.setChecked(False)
    self.extraction_tool_texture.setChecked(False)
    self.extraction_tool_color.setChecked(False)
    self.shapefile_tool_load.setChecked(False)

    excavation_layers.clear()
    segmentation_extraction_clipped_layers.clear()
    segmentation_extraction_layers.clear()
    shapefiles_layers.clear()
    shapefiles_clipped_and_subdivided_layers.clear()

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

    self.shapefile_tool_load_button.hide()
    self.shapefile_tool_scroll_area.hide()
    self.shapefile_tool_info_panel.setChecked(False)

    # check for found/-s
    if self.founds_show_hide.isChecked():
        self.check_founds()

    # plot textures oder colors
    if state:
        if self.excavation_side_texture.isChecked() and excavation_semaphor[0] != 0:
            excavation_semaphor[0] = 0
            self.clear_tool(use='excavation_side', tex_or_col='tex')
            if original_layers:
                for idx, (mesh_name, mesh_data, tex) in enumerate(zip(original_layers.keys(),
                                                                      original_layers.values(), textures)):
                    excavation_layers[mesh_name] = self.plotter.add_mesh(mesh=mesh_data, name=mesh_name,
                                                                         texture=tex, label=mesh_name)
            self.build_legend(do='remove')
        elif self.excavation_side_color.isChecked() and excavation_semaphor[0] != 1:
            excavation_semaphor[0] = 1
            self.clear_tool(use='excavation_side', tex_or_col='col')
            if original_layers:
                for idx, (mesh_name, mesh_data, color) in enumerate(zip(original_layers.keys(),
                                                                        original_layers.values(), colors)):
                    excavation_layers[mesh_name] = self.plotter.add_mesh(mesh=mesh_data, name=mesh_name,
                                                                         color=color, label=mesh_name)
            self.build_legend(do='add')
