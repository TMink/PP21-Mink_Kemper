# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import buttons_in_plot, interaction_objects_loaded, interaction_objects
from data.lists import clicked_somewhere_else, clicked, clicked_tracked, button_selected


def do(self, click):
    clicked_somewhere_else[0] += 1
    if clicked[0] > clicked_tracked[0]:
        clicked_tracked[0] = clicked[0]
    elif clicked[0] < clicked_somewhere_else[0]:
        for key, value in buttons_in_plot.items():
            for key2, value2 in interaction_objects_loaded.items():
                for key3, value3 in interaction_objects.items():
                    if button_selected[0][:button_selected[0].rfind('_')] == key3:
                        shrunk2 = value3
                        value2.overwrite(shrunk2)
            value.setStyleSheet(
                open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
        clicked_somewhere_else[0] += 1
        print(self.plotter.pick_click_position())
