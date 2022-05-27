# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import dummy_layer, decimated_layers


def do(self):
    # For the clipping algorithm to work, a mesh, where the plane/box widget can itself attach to, must preexist.
    # Therefore an invisible dummy is created.
    dummy_layer['dummy_layer_0'] = self.plotter.add_mesh(mesh=next(iter(decimated_layers.items()))[1],
                                                         name='dummy_layer_0', opacity=0.0,
                                                         show_scalar_bar=False, reset_camera=False)
