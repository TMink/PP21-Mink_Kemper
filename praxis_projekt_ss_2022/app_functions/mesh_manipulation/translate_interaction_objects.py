# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import original_layers


# translates to the center of the first layer in original_layers
def do(data: list):
    for elem in data:
        elem.translate(next(iter(original_layers.items()))[1].center, inplace=True)
