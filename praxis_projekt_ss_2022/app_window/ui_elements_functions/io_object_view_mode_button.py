# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Changes the interaction-style of the plotter.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import interaction_objects, interaction_objects_plotted, excavation_layers
from data.lists import interaction_style


def do(self):
    if interaction_style[0] == 0 and interaction_objects:
        self.plotter.enable_trackball_actor_style()
        self.plotter.pickable_actors = interaction_objects_plotted.values()
        interaction_style[0] = 1
    elif interaction_style[0] == 1 and interaction_objects:
        self.plotter.enable_trackball_style()
        self.plotter.pickable_actors = excavation_layers.values()
        interaction_style[0] = 0
