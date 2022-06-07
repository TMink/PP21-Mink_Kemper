# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Hides the checkbox, if corresponding found is not in plot.
"""
# ---------------------------------------------------------------------------
from data.dictionarys import shapefiles_checkboxes


def do(pos=None):
    for elem in shapefiles_checkboxes.values():
        if elem.objectName() == 'checkbox_%d' % pos:
            elem.hide()
