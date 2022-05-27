# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------


def do(data: dict, coords: list, names: list):
    hello_there = next(iter(data.items()))[1].center
    hello_again = [next(iter(data.items()))[1].center[0] + 1, next(iter(data.items()))[1].center[1],
                   next(iter(data.items()))[1].center[2]]
    coords.append(hello_there)
    coords.append(hello_again)
    names.append('Hello there!')
    names.append('Hello again!')
