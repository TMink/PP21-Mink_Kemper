import shutil
from app_functions.search_for_format import search_for_format

UTM_PATH = 'models/utm_coords/'
SHIFT_PATH = 'models/shift_coords/obj_format/'


def utm_to_shift():
    decimal_places = 6

    # list the current items in specific format
    utm_obj_list = search_for_format(UTM_PATH, ['obj'], cut=False)
    utm_rest_list = search_for_format(UTM_PATH, ['jpg', 'mtl'], cut=False)
    shift_obj_list = search_for_format(SHIFT_PATH, ['obj'], cut=False)
    shift_rest_list = search_for_format(SHIFT_PATH, ['jpg', 'mtl'], cut=False)

    # list every new item, that isnt already processed
    new_obj = [elem for elem in utm_obj_list if elem not in shift_obj_list]
    new_rest = [elem for elem in utm_rest_list if elem not in shift_rest_list]

    if new_obj and new_rest:

        # copy all non .obj files
        for elem in new_rest:
                shutil.copyfile(UTM_PATH + elem, SHIFT_PATH + elem)

        # global shift all .obj files
        for utm_elem in new_obj:
            utm = open(UTM_PATH + utm_elem, 'r')
            shift = open(SHIFT_PATH + utm_elem, 'w')
            count = 0
            for line in utm:
                if line.startswith('#'):
                    shift.write("# Shift Coords")
                if line.startswith('v '):
                    count += 1
                    groups = line.split(" ")
                    new_X = round(((float(groups[1]) / 100) - int(float(groups[1]) / 100)) * 100, decimal_places)
                    new_Y = round(((float(groups[2]) / 100) - int(float(groups[2]) / 100)) * 100, decimal_places)
                    content = '%s %s %s %s %s %s %s' % (
                        groups[0], str(new_X), str(new_Y), groups[3], groups[4], groups[5], groups[6])
                    shift.write(content)
                else:
                    shift.write(line)
