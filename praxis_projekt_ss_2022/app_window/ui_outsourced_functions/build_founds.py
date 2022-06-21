# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Sows and hides given founds in plot, if any mesh is plotted.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import excavation_layers, segmentation_extraction_clipped_layers, shapefiles_layers, \
    shapefiles_clipped_layers, founds, segmentation_extraction_layers


def do(self, state=None):
    if excavation_layers or segmentation_extraction_layers or segmentation_extraction_clipped_layers:
        if state:
            if excavation_layers or segmentation_extraction_clipped_layers or shapefiles_layers or \
                    shapefiles_clipped_layers:
                self.check_founds()
        else:
            self.plotter.remove_actor(founds.keys())
    else:
        self.founds_show_hide.setChecked(False)
