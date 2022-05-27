# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import pyvista as pv

from app_functions.general import calculate_volume_between
from data.dictionarys import excavation_layers, segmentation_extraction_clipped_layers, \
    segmentation_extraction_layers, shapefiles_layers, shapefiles, decimated_layers, shapefiles_clipped_layers
from data.lists import shapefile_semaphor, textures, colors


def do(self, state):
    # clear and reset
    self.plotter.remove_actor(excavation_layers.keys())
    self.plotter.remove_actor(segmentation_extraction_clipped_layers.keys())
    self.plotter.remove_actor(segmentation_extraction_layers.keys())
    self.plotter.remove_actor(shapefiles_layers.keys())

    self.plotter.clear_plane_widgets()
    self.plotter.clear_box_widgets()

    self.excavation_side_textures.setChecked(False)
    self.excavation_side_color.setChecked(False)
    self.segmentation_tool_texture.setChecked(False)
    self.segmentation_tool_color.setChecked(False)
    self.extraction_tool_texture.setChecked(False)
    self.extraction_tool_color.setChecked(False)

    excavation_layers.clear()
    segmentation_extraction_clipped_layers.clear()
    segmentation_extraction_layers.clear()
    shapefiles_layers.clear()

    self.interaction_objects_info_panel.setChecked(False)
    self.interactable_objects_label.hide()
    self.interactable_accessible_objects_scroll_area.hide()

    # testing ... irrelevant with real shapefiles
    shapefile = pv.Tube(radius=2.0)
    shapefiles['test_shapefile'] = shapefile
    shapefile.rotate_y(90, inplace=True)
    shapefile.translate(next(iter(decimated_layers.items()))[1].center, inplace=True)

    # clip decimated_meshes with shapefile
    for key, value in decimated_layers.items():
        shapefiles_clipped_layers[key] = value.clip_surface(shapefile, invert=True)

    # calculate volume between meshes
    calculate_volume_between(first_layer='15_17-07', second_layer='18_17-07')

    # plot textures or colors
    if state:
        if self.shapefile_tool_texture.isChecked() and shapefile_semaphor[0] != 0:
            shapefile_semaphor[0] = 0
            self.clear_tool(use='shapefile_tool', tex_or_col='tex')
            if shapefiles_clipped_layers:
                for idx, (clipped_name, clipped_data, tex) in enumerate(zip(shapefiles_clipped_layers.keys(),
                                                                            shapefiles_clipped_layers.values(),
                                                                            textures)):
                    shapefiles_layers[clipped_name] = self.plotter.add_mesh(mesh=clipped_data, name=clipped_name,
                                                                            texture=tex, label=clipped_name)
            self.legend(do='remove')
        elif self.shapefile_tool_color.isChecked() and shapefile_semaphor[0] != 1:
            shapefile_semaphor[0] = 1
            self.clear_tool(use='shapefile_tool', tex_or_col='col')
            if shapefiles_clipped_layers:
                for idx, (clipped_name, clipped_data, color) in enumerate(zip(shapefiles_clipped_layers.keys(),
                                                                              shapefiles_clipped_layers.values(),
                                                                              colors)):
                    shapefiles_layers[clipped_name] = self.plotter.add_mesh(mesh=clipped_data, name=clipped_name,
                                                                            color=color, label=clipped_name)
            self.legend(do='add')

    # check for found/-s
    if self.founds_show_hide.isChecked():
        self.check_founds()
