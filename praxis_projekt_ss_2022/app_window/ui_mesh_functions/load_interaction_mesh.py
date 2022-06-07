# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import pyvista as pv

from data.dictionarys import excavation_layers, segmentation_extraction_clipped_layers, original_layers
from data.lists import interaction_actors, plotted_interaction_actors


def do(self):
    if excavation_layers or segmentation_extraction_clipped_layers:
        interaction_actors.clear()
        plotted_interaction_actors.clear()
        # self.hide_show_interaction_side_panel()
        mesh = pv.Cube()
        name = 'Cube'
        mesh.translate(next(iter(original_layers.items()))[1].center, inplace=True)
        plotted_interaction_actors.append(self.plotter.add_mesh(mesh=mesh, name=name))
        interaction_actors.append(name)
