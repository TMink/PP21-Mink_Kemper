# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5.QtCore import Qt

from app_functions.general import change_found_color
from data.lists import colored_founds


def do(self, state=None):
    if Qt.Checked == state:
        change_found_color()
        self.ui_outsourced_functions['check_founds'](self, colored=colored_founds)
        self.founds_show_hide.setChecked(True)
        self.found_label.setText('Interactionmode On')
    else:
        change_found_color()
        self.ui_outsourced_functions['check_founds'](self, colored=colored_founds)
        self.founds_show_hide.setChecked(True)
        self.found_label.setText('Interactionmode Off')
