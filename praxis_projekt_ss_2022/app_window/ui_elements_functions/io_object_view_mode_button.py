# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Changes the interaction-style of the plotter.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import interaction_objects, interaction_objects_plotted, excavation_layers, \
    segmentation_extraction_layers, segmentation_extraction_clipped_layers
from data.lists import interaction_style, button_selected


def do(self):
    if excavation_layers or segmentation_extraction_layers or segmentation_extraction_clipped_layers:
        if interaction_style[0] == 0 and interaction_objects:
            self.plotter.enable_trackball_actor_style()
            self.plotter.pickable_actors = interaction_objects_plotted.values()
            self.interaction_objects_object_view_mode_button.setStyleSheet(
                open('resources/style_sheets/button_selected_style_sheet.txt').read().replace('\n', ''))
            interaction_style[0] = 1
        elif interaction_style[0] == 1 and interaction_objects:
            self.plotter.enable_trackball_style()
            self.plotter.pickable_actors = excavation_layers.values()
            self.interaction_objects_object_view_mode_button.setStyleSheet(
                open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
            interaction_style[0] = 0
