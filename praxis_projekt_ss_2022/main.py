# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from alive_progress import alive_bar

import app_tasks.tasks
from app_tasks.tasks import compute, task_quantity


def main():

    with alive_bar(task_quantity(), force_tty=True, theme='classic') as bar:
        for i in compute():
            bar()

    app_tasks.tasks.tasks['start']()


if __name__ == '__main__':
    main()
