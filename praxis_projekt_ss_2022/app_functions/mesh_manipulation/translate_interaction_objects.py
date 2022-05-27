# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import decimated_layers


# translates to the center of the first layer in decimated_layers
def do(data: list):
    for elem in data:
        elem.translate(next(iter(decimated_layers.items()))[1].center, inplace=True)
