# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout


def do(self):

    layout = QVBoxLayout()
    self.setLayout(layout)

    layout.addWidget(self.frame)

    # system name
    self.system_name.resize(self.width() - 10, 200)
    self.system_name.move(0, 40)
    self.system_name.setObjectName('system_name')
    self.system_name.setText('Colonia MeshUp')
    self.system_name.setAlignment(Qt.AlignCenter)
    self.system_name.setFont(QFont('Castellar'))

    # current task
    self.current_task.resize(self.width() - 10, 50)
    self.current_task.move(0, self.system_name.height())
    self.current_task.setObjectName('current_task')
    self.current_task.setText('<strong>Working on task #1</strong>')
    self.current_task.setAlignment(Qt.AlignCenter)
    self.current_task.setFont(QFont('helvetiker regular'))

    # progressbar
    self.progressbar.resize(self.width() - 200 - 10, 50)
    self.progressbar.move(100, self.current_task.y() + 130)
    self.progressbar.setAlignment(Qt.AlignCenter)
    self.progressbar.setFormat('%p%')
    self.progressbar.setVisible(True)
    self.progressbar.setRange(0, self.n)
    self.progressbar.setValue(20)

    # loading sign
    self.loading_sign.resize(self.width() - 10, 50)
    self.loading_sign.move(0, self.progressbar.y() + 70)
    self.loading_sign.setObjectName('loading_sign')
    self.loading_sign.setAlignment(Qt.AlignCenter)
    self.loading_sign.setText('loading...')
    self.loading_sign.setFont(QFont('helvetiker regular'))
