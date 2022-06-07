# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import shapefiles_checkboxes


def do(pos=None):
    for elem in shapefiles_checkboxes.values():
        if elem.objectName() == 'checkbox_%d' % pos:
            elem.hide()
