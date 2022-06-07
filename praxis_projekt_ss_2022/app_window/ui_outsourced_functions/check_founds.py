# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Checks, if founds should be visible in plot. If the mesh is clipped, every founds which are not in the extant part of
the mesh are deleted from the plot.
"""
# ---------------------------------------------------------------------------
import pyvista as pv

from data.dictionarys import founds, segmentation_extraction_clipped_layers, shapefiles_layers, original_layers, \
    shapefiles
from data.lists import found_coordinates, found_names, colored_founds


def do(self):

    checked_seg_ex = [
        self.segmentation_tool_texture.isChecked(),
        self.segmentation_tool_color.isChecked(),
        self.extraction_tool_texture.isChecked(),
        self.extraction_tool_color.isChecked(),
    ]

    checked_shp = [
        self.shapefile_tool_load.isChecked()
    ]

    box = None

    visible_founds = {}
    points_poly = pv.PolyData(found_coordinates)

    self.plotter.remove_actor(founds.keys())
    founds.clear()

    if not any(checked_seg_ex) and not any(
            checked_shp) and not segmentation_extraction_clipped_layers and not shapefiles_layers:
        item = next(iter(original_layers.items()))[1]
        box = pv.Box(item.bounds)
    elif not any(checked_shp) and not shapefiles_layers:
        box = pv.Box(segmentation_extraction_clipped_layers['clipped_layer_0'].bounds)
    elif not any(checked_seg_ex) and not segmentation_extraction_clipped_layers:
        box = list(shapefiles.values())[0].fill_holes(100, inplace=True)

    select = points_poly.select_enclosed_points(box)
    points_inside_box = select['SelectedPoints']

    # show/hide checkboxes
    count_dooku = 0
    for elem in points_inside_box:
        if elem == 0:
            self.f_checkbox_hide(count_dooku)
            count_dooku += 1
        if elem == 1:
            self.f_checkbox_show(count_dooku)
            count_dooku += 1

    for selected, point, name in zip(points_inside_box, found_coordinates, found_names):
        if selected == 1:
            visible_founds[name] = point

    if 1 in points_inside_box:
        for idx, key in enumerate(visible_founds):
            name = 'found_{}'.format(idx)
            color = 'white'
            if colored_founds:
                for elem in colored_founds:
                    if key == elem:
                        color = 'green'
            founds[name] = self.plotter.add_point_labels(points=[visible_founds[key]], labels=[key],
                                                         point_size=20, font_size=36, name=name,
                                                         reset_camera=False, text_color=color, fill_shape=False)
