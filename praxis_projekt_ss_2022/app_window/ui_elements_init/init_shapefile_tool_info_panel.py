# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------


def do(self):

    self.shapefile_tool_label.setLayout(self.shapefile_tool_layout)

    self.shapefile_tool_layout.addWidget(self.volume_label)
    self.shapefile_tool_layout.addItem(self.spacer_item)

    self.shapefile_tool_label.setFixedWidth(500)
    self.shapefile_tool_label.setStyleSheet(
        open('resources/style_sheets/shapefile_tool_info_panel_styl_sheet.txt').read().replace('\n', ''))
    self.shapefile_tool_label.hide()

    self.info_panel_layout.addWidget(self.shapefile_tool_label)
