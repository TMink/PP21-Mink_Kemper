# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5.QtCore import Qt

from app_functions.general import change_shapefile_color


def do(self, state=None):
    if Qt.Checked == state:
        change_shapefile_color.do(self)
    else:
        change_shapefile_color.do(self)
