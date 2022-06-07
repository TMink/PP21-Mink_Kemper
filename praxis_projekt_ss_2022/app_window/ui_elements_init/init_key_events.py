# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Key events
"""
# ---------------------------------------------------------------------------


def do(self):
    self.plotter.add_key_event('F1', self.view_reset)
    self.plotter.add_key_event('F2', self.view_top)
    self.plotter.add_key_event('F3', self.view_bottom)
    self.plotter.add_key_event('F4', self.view_left)
    self.plotter.add_key_event('F5', self.view_right)
    self.plotter.add_key_event('F6', self.view_front)
    self.plotter.add_key_event('F7', self.view_back)
