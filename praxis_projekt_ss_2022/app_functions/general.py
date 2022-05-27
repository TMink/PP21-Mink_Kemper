# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import *
from data.lists import *


# checks wich checkbox is clicked and updates colored_labels withe corresponding name of the label
def change_found_color():
    for checkbox_key, checkbox_value in zip(check_boxes.keys(), check_boxes.values()):
        for labels_checkboxes_key, labels_checkboxes_value in zip(founds_checkboxes.keys(), founds_checkboxes.values()):
            if checkbox_key == labels_checkboxes_key:
                if checkbox_value.isChecked():
                    if colored_founds:
                        exist = colored_founds.count(labels_checkboxes_value)
                        if not exist:
                            colored_founds.append(labels_checkboxes_value)
                    else:
                        colored_founds.append(labels_checkboxes_value)
                else:
                    exist = colored_founds.count(labels_checkboxes_value)
                    if exist:
                        colored_founds.remove(labels_checkboxes_value)


# calculate volume between layers
def calculate_volume_between(first_layer: str, second_layer: str):
    volume.append(original_layers[first_layer].volume - original_layers[second_layer].volume)
