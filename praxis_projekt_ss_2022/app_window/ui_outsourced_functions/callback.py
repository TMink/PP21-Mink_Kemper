# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Callback
"""
# ---------------------------------------------------------------------------
from data.dictionarys import interaction_objects, buttons_in_plot
from data.lists import clicked


def do(mesh=None):
    for key, value in interaction_objects.items():
        if value == mesh:
            for key2, value2 in buttons_in_plot.items():
                if key2 == key:
                    value2.setStyleSheet(
                        open('resources/style_sheets/button_selected_style_sheet.txt').read().replace('\n', ''))
    clicked[0] += 1
