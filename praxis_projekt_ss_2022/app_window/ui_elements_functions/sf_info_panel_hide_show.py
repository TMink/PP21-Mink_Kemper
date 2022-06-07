# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import original_layers
from data.lists import volume


def do(self):
    if self.shapefile_tool_load_button.isHidden() and self.shapefile_tool_scroll_area.isHidden() and self.shapefile_tool_load.isChecked():
        self.shapefile_tool_load_button.show()
        self.shapefile_tool_scroll_area.show()
        self.shapefile_tool_info_panel.setChecked(True)

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

    else:
        self.shapefile_tool_load_button.hide()
        self.shapefile_tool_scroll_area.hide()
        self.shapefile_tool_info_panel.setChecked(False)
