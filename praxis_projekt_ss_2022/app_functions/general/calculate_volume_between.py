# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import original_layers
from data.lists import volume


def do(first_layer: str, second_layer: str):
    volume.append(original_layers[first_layer].volume - original_layers[second_layer].volume)
