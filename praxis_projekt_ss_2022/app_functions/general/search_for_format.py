# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Searches for a given format and returns the a list with 'filename.format' or 'name'
"""
# ---------------------------------------------------------------------------
import os


# searches for files with specific format
def search_for_format(path: str, format_type: [str], cut: bool):
    obj_list = []
    content_list = os.listdir(path)
    for elem in content_list:
        if any(word in elem for word in format_type):
            if cut:
                obj_list.append(elem[:elem.rfind('.')])
            else:
                obj_list.append(elem)
    return obj_list

#def search_for_format(path: str, format_type: [str], cut: bool, exceptions=None):
#    if exceptions is None:
#        exceptions = ['Stelio_Kantos']
#    obj_list = []
#    content_list = os.listdir(path)
#    for elem in content_list:
#        if any(word in elem for word in format_type) and not any(word in elem for word in exceptions):
#            if cut:
#                obj_list.append(elem[:elem.rfind('.')])
#            else:
#                obj_list.append(elem)
#    return obj_list
