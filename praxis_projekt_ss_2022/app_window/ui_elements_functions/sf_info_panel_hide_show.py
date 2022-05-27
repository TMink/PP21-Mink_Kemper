# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import decimated_layers
from data.lists import volume


def do(self):
    if self.shapefile_tool_label.isHidden():
        self.shapefile_tool_label.show()
        self.shapefile_tool_info_panel.setChecked(True)
        self.volume_label.setText(
            f'Volume between {list(decimated_layers.keys())[0]} and {list(decimated_layers.keys())[0]} is {volume[0]}')

        self.interactable_objects_label.hide()
        self.interactable_accessible_objects_scroll_area.hide()
        self.interactable_loaded_objects_scroll_area.hide()
        self.interactable_objects_create_button.hide()
        self.interactable_objects_delete_button.hide()
        self.interactable_objects_object_view_mode_button.hide()
        self.interaction_objects_info_panel.setChecked(False)

        self.found_label.hide()
        self.found_scroll_area.hide()
        self.founds_info_panel.setChecked(False)

    else:
        self.shapefile_tool_label.hide()
        self.shapefile_tool_info_panel.setChecked(False)
