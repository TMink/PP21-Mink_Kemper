# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Hides the checkbox, if corresponding found is not in plot.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import check_boxes


def do(pos=None):
    for elem in check_boxes.values():
        if elem.objectName() == 'checkbox_%d' % pos:
            elem.hide()
