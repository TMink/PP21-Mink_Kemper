# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------


def do(self):
    if self.found_label.isHidden() and self.found_scroll_area.isHidden():
        self.shapefile_tool_label.hide()
        self.shapefile_tool_info_panel.setChecked(False)

        self.interactable_objects_label.hide()
        self.interactable_accessible_objects_scroll_area.hide()
        self.interactable_loaded_objects_scroll_area.hide()
        self.interactable_objects_create_button.hide()
        self.interactable_objects_delete_button.hide()
        self.interactable_objects_object_view_mode_button.hide()
        self.interaction_objects_info_panel.setChecked(False)

        self.found_label.show()
        self.found_scroll_area.show()
        self.founds_info_panel.setChecked(True)
    else:
        self.found_label.hide()
        self.found_scroll_area.hide()
        self.founds_info_panel.setChecked(False)
