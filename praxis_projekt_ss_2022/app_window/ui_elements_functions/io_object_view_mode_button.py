# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import interactable_objects, interactable_objects_plotted, excavation_layers
from data.lists import interaction_style


def do(self):
    if interaction_style[0] == 0 and interactable_objects:
        self.plotter.enable_trackball_actor_style()
        self.plotter.pickable_actors = interactable_objects_plotted.values()
        interaction_style[0] = 1
    elif interaction_style[0] == 1 and interactable_objects:
        self.plotter.enable_trackball_style()
        self.plotter.pickable_actors = excavation_layers.values()
        interaction_style[0] = 0
