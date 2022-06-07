# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Info panel: interaction objects
"""
# ---------------------------------------------------------------------------
from functools import partial

from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton

from data.dictionarys import interaction_objects, buttons_not_in_plot


def do(self):
    # label
    self.interaction_objects_label.setStyleSheet(
        open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
    self.interaction_objects_label.setFont(QFont('helvetiker regular', 15))
    #self.interaction_objects_label.setText('')
    self.interaction_objects_label.setAutoFillBackground(True)
    self.interaction_objects_label.setFixedWidth(500)
    self.interaction_objects_label.setFixedHeight(100)
    self.interaction_objects_label.hide()

    # object/view mode
    self.interaction_objects_object_view_mode_button.clicked.connect(self.io_object_view_mode_button)
    self.interaction_objects_object_view_mode_button.setFixedWidth(500)
    self.interaction_objects_object_view_mode_button.setFixedHeight(40)
    self.interaction_objects_object_view_mode_button.setStyleSheet(
        open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
    self.interaction_objects_object_view_mode_button.hide()

    # create button
    self.interaction_objects_create_button.clicked.connect(self.io_create_not_plotted_objects_button)
    self.interaction_objects_create_button.clicked.connect(self.io_create_plotted_objects_button)
    self.interaction_objects_create_button.setFixedWidth(244)
    self.interaction_objects_create_button.setFixedHeight(40)
    self.interaction_objects_create_button.setStyleSheet(
        open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
    self.interaction_objects_create_button.hide()

    # delete button
    self.interaction_objects_delete_button.clicked.connect(self.io_delete_button)
    self.interaction_objects_delete_button.setFixedWidth(244)
    self.interaction_objects_delete_button.setFixedHeight(40)
    self.interaction_objects_delete_button.setStyleSheet(
        open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
    self.interaction_objects_delete_button.hide()

    column = 0
    row = 0

    for key, value in interaction_objects.items():
        button = QPushButton(key)
        button.setObjectName(key)
        button.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
        button.setFixedWidth(100)
        button.setFixedHeight(114)
        button.clicked.connect(partial(self.io_change_button_style, key))
        buttons_not_in_plot[key] = button

    for idx, value in enumerate(buttons_not_in_plot.values()):
        if idx % 2 == 0 and idx != 0:
            row += 1
        self.interaction_accessible_objects_scroll_area_layout.addWidget(value, row, column)
        column += 1
        if column > 1:
            column = 0

    self.interaction_accessible_objects_scroll_area_layout.addItem(self.spacer_item)

    self.interaction_accessible_objects_scroll_area_widget.setLayout(
        self.interaction_accessible_objects_scroll_area_layout)

    self.interaction_accessible_objects_scroll_area.setWidgetResizable(True)
    self.interaction_accessible_objects_scroll_area.setFixedWidth(244)
    self.interaction_accessible_objects_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.interaction_accessible_objects_scroll_area.setStyleSheet(
        open('resources/style_sheets/scroll_area_style_sheet.txt').read().replace('\n', ''))
    self.interaction_accessible_objects_scroll_area.hide()
    self.interaction_accessible_objects_scroll_area.setWidget(
        self.interaction_accessible_objects_scroll_area_widget)

    # scroll area loaded objects
    self.interaction_loaded_objects_scroll_area_widget.setLayout(
        self.interaction_loaded_objects_scroll_area_layout)

    self.interaction_loaded_objects_scroll_area.setWidgetResizable(True)
    self.interaction_loaded_objects_scroll_area.setFixedWidth(244)
    self.interaction_loaded_objects_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.interaction_loaded_objects_scroll_area.setStyleSheet(
        open('resources/style_sheets/scroll_area_style_sheet.txt').read().replace('\n', ''))
    self.interaction_loaded_objects_scroll_area.hide()
    self.interaction_loaded_objects_scroll_area.setWidget(
        self.interaction_loaded_objects_scroll_area_widget)

    self.interaction_objects_create_delete_button_layout.addWidget(self.interaction_objects_delete_button)
    self.interaction_objects_create_delete_button_layout.addWidget(self.interaction_objects_create_button)

    self.interaction_objects_scroll_areas_layout.addWidget(self.interaction_loaded_objects_scroll_area)
    self.interaction_objects_scroll_areas_layout.addWidget(self.interaction_accessible_objects_scroll_area)

    self.info_panel_layout.addWidget(self.interaction_objects_label)
    self.info_panel_layout.addWidget(self.interaction_objects_object_view_mode_button)
    self.info_panel_layout.addLayout(self.interaction_objects_create_delete_button_layout)
    self.info_panel_layout.addLayout(self.interaction_objects_scroll_areas_layout)
