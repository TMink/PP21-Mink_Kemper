# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------

from data.dictionarys import *
from data.lists import *

# rotates the content of decimated_meshes at an 50 degree angle around the z-axis
def rotate(data: list):
    #z = next(iter(decimated_meshes.items()))[1].center[2] * -1.0
    #x = next(iter(decimated_meshes.items()))[1].center[0] * -1.0
    #y = next(iter(decimated_meshes.items()))[1].center[1] * -1.0
    for elem in data:
        #elem.translate((x, y, z), inplace=True)
        elem.rotate_z(50.0, inplace=True)


# testing
def labels(data: dict, coords: list, names: list):
    hello_there = next(iter(data.items()))[1].center
    hello_again = [next(iter(data.items()))[1].center[0] + 1, next(iter(data.items()))[1].center[1],
                   next(iter(data.items()))[1].center[2]]
    coords.append(hello_there)
    coords.append(hello_again)
    names.append('Hello there!')
    names.append('Hello again!')


# checks wich checkbox is clicked and updates colored_labels withe corresponding name of the label
def change_label_color():
    for checkbox_key, checkbox_value in zip(check_boxes.keys(), check_boxes.values()):
        for labels_checkboxes_key, labels_checkboxes_value in zip(labels_checkboxes.keys(), labels_checkboxes.values()):
            if checkbox_key == labels_checkboxes_key:
                if checkbox_value.isChecked():
                    if colored_labels:
                        exist = colored_labels.count(labels_checkboxes_value)
                        if not exist:
                            colored_labels.append(labels_checkboxes_value)
                    else:
                        colored_labels.append(labels_checkboxes_value)
                else:
                    exist = colored_labels.count(labels_checkboxes_value)
                    if exist:
                        colored_labels.remove(labels_checkboxes_value)
