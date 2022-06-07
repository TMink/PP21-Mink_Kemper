# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import interaction_objects_plotted, buttons_in_plot
from data.lists import button_selected


def do(self):
    found = [val for key, val in interaction_objects_plotted.items() if button_selected[0] == key]
    key_item = '_'
    if found:
        for key, value in interaction_objects_plotted.items():
            if value == found[0]:
                self.plotter.remove_actor(key)
                key_item = key
        interaction_objects_plotted.pop(key_item)
        buttons_in_plot[key_item].deleteLater()
        buttons_in_plot.pop(key_item)
        button_selected[0] = '_'
