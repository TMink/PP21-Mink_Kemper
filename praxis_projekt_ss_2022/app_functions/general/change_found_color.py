# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import check_boxes, founds_checkboxes
from data.lists import colored_founds


def do():
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
