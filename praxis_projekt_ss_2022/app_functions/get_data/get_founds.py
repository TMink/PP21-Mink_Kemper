# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Gets all data relatet to 'founds' and saves them into cords and names. At the moment there are only examples of
possible data.
"""
# ---------------------------------------------------------------------------


def do(data: dict, cords: list, names: list):
    found_one = next(iter(data.items()))[1].center
    found_two = [next(iter(data.items()))[1].center[0] + 1, next(iter(data.items()))[1].center[1],
                   next(iter(data.items()))[1].center[2]]
    cords.append(found_one)
    cords.append(found_two)
    names.append('found_one')
    names.append('found_two')
