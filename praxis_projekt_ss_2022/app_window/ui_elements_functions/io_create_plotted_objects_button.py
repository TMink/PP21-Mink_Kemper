# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Creates a button for every interaction object in plot.
"""
# ---------------------------------------------------------------------------
from functools import partial

from PyQt5.QtWidgets import QPushButton

from data.dictionarys import interaction_objects_plotted, buttons_in_plot, excavation_layers, \
    segmentation_extraction_layers, segmentation_extraction_clipped_layers
from data.lists import button_selected


def do(self):
    if button_selected[0] != '_' and (excavation_layers or segmentation_extraction_layers or
                                      segmentation_extraction_clipped_layers):
        button = QPushButton(f'{list(interaction_objects_plotted.keys())[-1]}')
        button.setObjectName(f'{list(interaction_objects_plotted.keys())[-1]}')
        button.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
        button.setFixedWidth(100)
        button.setFixedHeight(114)
        button.clicked.connect(partial(self.io_change_button_style, f'{list(interaction_objects_plotted.keys())[-1]}'))
        buttons_in_plot[f'{list(interaction_objects_plotted.keys())[-1]}'] = button

        row = 0
        column = 0

        for idx, value in enumerate(buttons_in_plot.values()):
            if idx % 2 == 0 and idx != 0:
                row += 1
            self.interaction_loaded_objects_scroll_area_layout.addWidget(value, row, column)
            column += 1
            if column > 1:
                column = 0

        self.interaction_loaded_objects_scroll_area_layout.addItem(self.spacer_item)
