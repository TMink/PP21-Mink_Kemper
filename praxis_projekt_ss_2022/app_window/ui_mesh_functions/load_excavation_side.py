# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import dummy_layer, excavation_layers, segmentation_extraction_clipped_layers, \
    segmentation_extraction_layers, shapefiles_layers, decimated_layers
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

    self.plotter.clear_plane_widgets()
    self.plotter.clear_box_widgets()

    self.segmentation_tool_texture.setChecked(False)
    self.segmentation_tool_color.setChecked(False)
    self.extraction_tool_texture.setChecked(False)
    self.extraction_tool_color.setChecked(False)
    self.shapefile_tool_texture.setChecked(False)
    self.shapefile_tool_color.setChecked(False)

    excavation_layers.clear()
    segmentation_extraction_clipped_layers.clear()
    segmentation_extraction_layers.clear()
    shapefiles_layers.clear()

    self.shapefile_tool_info_panel.setChecked(False)
    self.shapefile_tool_label.hide()

    # check for found/-s
    if self.founds_show_hide.isChecked():
        self.check_founds()

    # plot textures oder colors
    if state:
        if self.excavation_side_texture.isChecked() and excavation_semaphor[0] != 0:
            excavation_semaphor[0] = 0
            self.clear_tool(use='excavation_side', tex_or_col='tex')
            if decimated_layers:
                for idx, (mesh_name, mesh_data, tex) in enumerate(zip(decimated_layers.keys(),
                                                                      decimated_layers.values(), textures)):
                    excavation_layers[mesh_name] = self.plotter.add_mesh(mesh=mesh_data, name=mesh_name,
                                                                         texture=tex, label=mesh_name)
            self.build_legend(do='remove')
        elif self.excavation_side_color.isChecked() and excavation_semaphor[0] != 1:
            excavation_semaphor[0] = 1
            self.clear_tool(use='excavation_side', tex_or_col='col')
            if decimated_layers:
                for idx, (mesh_name, mesh_data, color) in enumerate(zip(decimated_layers.keys(),
                                                                        decimated_layers.values(), colors)):
                    excavation_layers[mesh_name] = self.plotter.add_mesh(mesh=mesh_data, name=mesh_name,
                                                                         color=color, label=mesh_name)
            self.build_legend(do='add')
