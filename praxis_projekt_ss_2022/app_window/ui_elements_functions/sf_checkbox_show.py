# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Shows the checkbox, if corresponding found is in plot.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import shapefiles_checkboxes


def do(self, pos=None):
    self.shapefile_tool_scroll_area_layout.removeItem(self.spacer_item)
    for elem in shapefiles_checkboxes.values():
        if elem.objectName() == 'checkbox_%d' % pos:
            elem.show()
    self.shapefile_tool_scroll_area_layout.addItem(self.spacer_item)
