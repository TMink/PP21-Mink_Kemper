# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Deletes widgets, resets the camera and deselect menu elements.
"""
# ---------------------------------------------------------------------------


def do(self, use: str, tex_or_col='_'):
    self.plotter.reset_camera()
    if use == 'segmentation_tool':
        if tex_or_col == 'tex':
            self.segmentation_tool_color.setChecked(False)
        if tex_or_col == 'col':
            self.segmentation_tool_texture.setChecked(False)
        self.plotter.clear_plane_widgets()
    if use == 'extraction_tool':
        if tex_or_col == 'tex':
            self.extraction_tool_color.setChecked(False)
        if tex_or_col == 'col':
            self.extraction_tool_texture.setChecked(False)
        self.plotter.clear_box_widgets()
    if use == 'excavation_side':
        if tex_or_col == 'tex':
            self.excavation_side_color.setChecked(False)
        if tex_or_col == 'col':
            self.excavation_side_texture.setChecked(False)
    if use == 'shapefile_tool':
        if tex_or_col == 'tex':
            self.shapefile_tool_color.setChecked(False)
        if tex_or_col == 'col':
            self.shapefile_tool_texture.setChecked(False)
