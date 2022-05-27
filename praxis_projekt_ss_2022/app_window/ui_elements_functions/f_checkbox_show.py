# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import check_boxes


def do(self, pos=None):
    self.found_scroll_area_layout.removeItem(self.spacer_item)
    for elem in check_boxes.values():
        if elem.objectName() == 'checkbox_%d' % pos:
            elem.show()
    self.found_scroll_area_layout.addItem(self.spacer_item)
