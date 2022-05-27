# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import excavation_layers, segmentation_extraction_clipped_layers, shapefiles_layers, \
    shapefiles_clipped_layers, founds


def do(self, state=None):
    if state:
        if excavation_layers or segmentation_extraction_clipped_layers or shapefiles_layers or shapefiles_clipped_layers:
            self.check_founds()
    else:
        self.plotter.remove_actor(founds.keys())
