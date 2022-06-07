# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Changes color of found in plot, shows founds and changes founds_label text.
"""
# ---------------------------------------------------------------------------
from PyQt5.QtCore import Qt

from app_functions.general import change_found_color


def do(self, state=None):
    if Qt.Checked == state:
        change_found_color.do()
        self.check_founds()
        self.founds_show_hide.setChecked(True)
        self.found_label.setText('Interactionmode On')
    else:
        change_found_color.do()
        self.check_founds()
        self.founds_show_hide.setChecked(True)
        self.found_label.setText('Interactionmode Off')
