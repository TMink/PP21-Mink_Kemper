# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Shapefile tool
"""
# ---------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5.QtWidgets import QCheckBox

from data.dictionarys import shapefiles, shapefiles_checkboxes


def do(self):
    # checkbox
    for key, value in shapefiles.items():
        checkbox = QCheckBox(key)
        checkbox.setObjectName(key)
        shapefiles_checkboxes[key] = checkbox

    for elem in shapefiles_checkboxes.values():
        elem.setStyleSheet(open('resources/style_sheets/checkbox_style_sheet.txt').read().replace('\n', ''))
        elem.setFixedWidth(459)
        elem.stateChanged.connect(self.sf_checkbox_action)

    # connect checkboxes to scroll area
    for elem in shapefiles_checkboxes.values():
        self.shapefile_tool_scroll_area_layout.addWidget(elem)

    # scroll area
    self.shapefile_tool_scroll_area_layout.addItem(self.spacer_item)
    self.shapefile_tool_scroll_area_widget.setLayout(self.shapefile_tool_scroll_area_layout)

    self.shapefile_tool_scroll_area.setWidgetResizable(True)
    self.shapefile_tool_scroll_area.setFixedWidth(500)
    self.shapefile_tool_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.shapefile_tool_scroll_area.setStyleSheet(
        open('resources/style_sheets/scroll_area_style_sheet.txt').read().replace('\n', ''))
    self.shapefile_tool_scroll_area.hide()
    self.shapefile_tool_scroll_area.setWidget(self.shapefile_tool_scroll_area_widget)

    # load button
    self.shapefile_tool_load_button.clicked.connect(self.sf_load_button)
    self.shapefile_tool_load_button.setFixedWidth(500)
    self.shapefile_tool_load_button.setFixedHeight(40)
    self.shapefile_tool_load_button.setStyleSheet(
        open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
    self.shapefile_tool_load_button.hide()

    self.info_panel_layout.addWidget(self.shapefile_tool_load_button)
    self.info_panel_layout.addWidget(self.shapefile_tool_scroll_area)
