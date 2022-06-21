# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Initialize the progressbar of the loading screen.
"""
# ---------------------------------------------------------------------------
import time

import app_tasks.tasks as tasks


def do(self, b):
    self.progressbar.setValue(0)

    tasks_to_do = tasks.tasks_names
    without_start = [func_name for func_name in tasks.tasks.keys()]
    without_start = without_start[:-1]
    for idx, (key, task) in enumerate(zip(without_start, tasks_to_do)):
        tasks.tasks[key]()
        self.current_task.setText(f'<strong> {task} </strong>')
        self.progressbar.setValue(idx * 10)

    self.timer.stop()
    self.close()
    time.sleep(0.5)
    self.myApp = b()
    self.myApp.show()
