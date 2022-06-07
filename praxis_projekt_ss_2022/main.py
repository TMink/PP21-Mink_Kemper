# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from alive_progress import alive_bar

import app_tasks.tasks



def main():

    app_tasks.tasks.tasks['start']()


if __name__ == '__main__':
    main()
