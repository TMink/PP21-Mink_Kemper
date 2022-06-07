# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import original_layers
from data.lists import colors


def do(self, task: str):
    if task == 'remove':
        self.plotter.remove_legend()
    if task == 'add':
        new_list = []
        for mesh_name, color in zip(original_layers.keys(), colors):
            new_list.append([mesh_name, color])
        self.plotter.add_legend(labels=new_list, bcolor='#0c1726', face="r", loc="upper left", size=(0.1, 0.1))
