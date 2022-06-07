# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Change the color of the shapefile, if the corresponding checkbox is clicked
"""
# ---------------------------------------------------------------------------
from data.dictionarys import shapefiles_checkboxes, shapefiles_layers, shapefiles, shapefiles_colors, \
    shapefiles_colors_actual, shapefiles_selected_for_clipping, shapefiles_clipped_and_subdivided_layers


def do(self):

    if not shapefiles_clipped_and_subdivided_layers:
        for shapefile_checkbox_key, shapefile_checkbox_value in shapefiles_checkboxes.items():
            if shapefile_checkbox_value.isChecked():
                self.plotter.remove_actor(shapefiles_layers[shapefile_checkbox_key])
                for key, value in shapefiles_colors.items():
                    if key == shapefile_checkbox_key[:shapefile_checkbox_key.rfind('_')]:
                        shapefiles_colors_actual[shapefile_checkbox_key] = value
                        shapefiles_layers[shapefile_checkbox_key] = self.plotter.add_mesh(
                            mesh=shapefiles[shapefile_checkbox_key], name=shapefile_checkbox_key, color=value, reset_camera=False)
                        shapefiles_selected_for_clipping[shapefile_checkbox_key] = shapefiles[shapefile_checkbox_key]
            elif not shapefile_checkbox_value.isChecked() and shapefiles_colors_actual[shapefile_checkbox_key] != 'white':
                self.plotter.remove_actor(shapefiles_layers[shapefile_checkbox_key])
                shapefiles_colors_actual[shapefile_checkbox_key] = 'white'
                shapefiles_layers[shapefile_checkbox_key] = self.plotter.add_mesh(
                    mesh=shapefiles[shapefile_checkbox_key], name=shapefile_checkbox_key, color='white', reset_camera=False)
                del shapefiles_selected_for_clipping[shapefile_checkbox_key]
