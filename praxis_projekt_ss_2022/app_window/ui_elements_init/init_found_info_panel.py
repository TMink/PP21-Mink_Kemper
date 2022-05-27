# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox

from data.dictionarys import check_boxes, founds_checkboxes
from data.lists import found_coordinates, found_names


def do(self):
    # label
    self.found_label.setStyleSheet(
        open('resources/style_sheets/label_style_sheet.txt').read().replace('\n', ''))
    self.found_label.setFont(QFont('helvetiker regular', 15))
    self.found_label.setText('Hello World')
    self.found_label.setAutoFillBackground(True)
    self.found_label.setFixedWidth(500)
    self.found_label.hide()
    self.info_panel_layout.addWidget(self.found_label, alignment=QtCore.Qt.AlignTop)

    # checkbox
    for i in range(0, len(found_coordinates)):
        checkbox = QCheckBox(found_names[i])
        checkbox.setObjectName(f'checkbox_{i}')
        check_boxes[f'checkbox_{i}'] = checkbox
        founds_checkboxes[f'checkbox_{i}'] = found_names[i]

    for elem in check_boxes.values():
        elem.setStyleSheet(open('resources/style_sheets/checkbox_style_sheet.txt').read().replace('\n', ''))
        elem.setFixedWidth(459)
        elem.stateChanged.connect(self.f_checkbox_action)

    # scroll area
    for elem in check_boxes.values():
        self.found_scroll_area_layout.addWidget(elem)

    self.found_scroll_area_layout.addItem(self.spacer_item)

    self.found_scroll_area_widget.setLayout(self.found_scroll_area_layout)

    self.found_scroll_area.setWidgetResizable(True)
    self.found_scroll_area.setFixedWidth(500)
    self.found_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
    self.found_scroll_area.setStyleSheet(
        open('resources/style_sheets/scroll_area_style_sheet.txt').read().replace('\n', ''))
    self.found_scroll_area.hide()
    self.found_scroll_area.setWidget(self.found_scroll_area_widget)

    self.info_panel_layout.addWidget(self.found_scroll_area)
