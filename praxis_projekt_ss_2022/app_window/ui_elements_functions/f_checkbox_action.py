# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5.QtCore import Qt

from app_functions.general import change_found_color


def do(self, state=None):
    print('test1')
    if Qt.Checked == state:
        print('test2')
        change_found_color.do()
        print('test3')
        self.check_founds()
        print('test4')
        self.founds_show_hide.setChecked(True)
        print('test5')
        self.found_label.setText('Interactionmode On')
    else:
        change_found_color.do()
        self.check_founds()
        self.founds_show_hide.setChecked(True)
        self.found_label.setText('Interactionmode Off')
