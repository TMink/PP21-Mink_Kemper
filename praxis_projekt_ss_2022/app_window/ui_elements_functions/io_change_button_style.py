# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import buttons_not_in_plot, interaction_objects_loaded, interaction_objects, buttons_in_plot
from data.lists import button_selected


def do(button_name=None):
    if not button_selected.count(button_name):
        button_selected[0] = button_name
        for key, value in buttons_not_in_plot.items():
            if key == button_name:
                for key2, value2 in interaction_objects_loaded.items():
                    for key3, value3 in interaction_objects.items():
                        if key2[:key2.rfind('_')] == key3:
                            shrunk = value3
                            value2.overwrite(shrunk)
                value.setStyleSheet(
                    open('resources/style_sheets/button_selected_style_sheet.txt').read().replace('\n', ''))
            if key != button_name:
                value.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
        for key, value in buttons_in_plot.items():
            if key == button_name:
                for key2, value2 in interaction_objects_loaded.items():
                    if key == key2:
                        shrunk = value2.outline()
                        value2.overwrite(shrunk)
                    else:
                        for key3, value3 in interaction_objects.items():
                            if button_selected[0][:button_selected[0].rfind('_')] == key3:
                                shrunk2 = value3
                                value2.overwrite(shrunk2)
                value.setStyleSheet(
                    open('resources/style_sheets/button_selected_style_sheet.txt').read().replace('\n', ''))
            if key != button_name:
                value.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
    else:
        button_selected[0] = '_'
        for key, value in buttons_not_in_plot.items():
            if key == button_name:
                value.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
        for key, value in buttons_in_plot.items():
            if key == button_name:
                for key2, value2 in interaction_objects_loaded.items():
                    if key == key2:
                        for key3, value3 in interaction_objects.items():
                            if key[:key.rfind('_')] == key3:
                                shrunk2 = value3
                                value2.overwrite(shrunk2)
                value.setStyleSheet(open('resources/style_sheets/buttons_style_sheet.txt').read().replace('\n', ''))
