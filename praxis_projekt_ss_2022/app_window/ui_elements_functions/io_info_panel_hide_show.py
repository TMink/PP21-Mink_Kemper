# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------


def do(self):
    if self.interaction_objects_label.isHidden():
        self.shapefile_tool_load_button.hide()
        self.shapefile_tool_scroll_area.hide()
        self.shapefile_tool_info_panel.setChecked(False)

        self.interaction_objects_label.show()
        self.interaction_accessible_objects_scroll_area.show()
        self.interaction_loaded_objects_scroll_area.show()
        self.interaction_objects_create_button.show()
        self.interaction_objects_delete_button.show()
        self.interaction_objects_object_view_mode_button.show()
        self.interaction_objects_info_panel.setChecked(True)

        self.found_label.hide()
        self.found_scroll_area.hide()
        self.founds_info_panel.setChecked(False)

    else:
        self.interaction_objects_label.hide()
        self.interaction_accessible_objects_scroll_area.hide()
        self.interaction_loaded_objects_scroll_area.hide()
        self.interaction_objects_create_button.hide()
        self.interaction_objects_delete_button.hide()
        self.interaction_objects_object_view_mode_button.hide()
        self.interaction_objects_info_panel.setChecked(False)
