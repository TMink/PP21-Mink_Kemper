# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Resize the labels of the side panels, corresponding to the window size.
"""
# ---------------------------------------------------------------------------


def do(self):
    self.found_label.setFixedHeight(self.height() / 2)
    self.interaction_objects_label.setFixedHeight(self.height() / 2)
