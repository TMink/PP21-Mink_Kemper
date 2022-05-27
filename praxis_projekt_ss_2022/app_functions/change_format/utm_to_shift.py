# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import shutil

from app_functions.search_for_format import search_for_format

from data.dictionarys import old_utm_coords


def do(utm_path: str, shift_path: str):
    global utm, shift
    run_once = True
    decimal_places = 6

    # list the current items in specific format
    utm_obj_list = search_for_format(utm_path, ['obj'], cut=True)
    utm_rest_list = search_for_format(utm_path, ['jpg', 'mtl'], cut=False)
    shift_obj_list = search_for_format(shift_path, ['obj'], cut=True)
    shift_rest_list = search_for_format(shift_path, ['jpg', 'mtl'], cut=False)

    # list every new item, that isnt already processed
    new_obj = [elem for elem in utm_obj_list if elem not in shift_obj_list]
    new_rest = [elem for elem in utm_rest_list if elem not in shift_rest_list]

    if new_obj and new_rest:

        # copy all non .obj files
        for elem in new_rest:
            try:
                shutil.copyfile(utm_path + elem, shift_path + elem)
            except OSError:
                print(f'cannot copy {elem} from {utm_path} to {shift_path}')

        # global shift all .obj files
        for idx, utm_elem in enumerate(new_obj):
            try:
                utm = open(utm_path + utm_elem + '.obj', 'r')
            except OSError:
                print(f'cannot open {utm_elem} from {utm_path}')

            try:
                shift = open(shift_path + utm_elem + '.obj', 'w')
            except OSError:
                print(f'cannot open {utm_elem} from {shift_path}')

            for line in utm:
                if line.startswith('#'):
                    shift.write("# Shift Coords")
                if line.startswith('v '):
                    groups = line.split(" ")
                    new_x = round(((float(groups[1]) / 100) - int(float(groups[1]) / 100)) * 100, decimal_places)
                    new_y = round(((float(groups[2]) / 100) - int(float(groups[2]) / 100)) * 100, decimal_places)
                    if run_once:
                        d = open(f'database/{utm_elem}.txt', 'w')
                        d.write(f'{f"layer_{idx}"} {f"{utm_elem}.txt"} {float(groups[1]) - new_x} '
                                f'{float(groups[2]) - new_y}')
                        d.close()
                        run_once = False
                    content = f'{groups[0]} {str(new_x)} {str(new_y)} {groups[3]} {groups[4]} {groups[5]} {groups[6]}'
                    shift.write(content)
                else:
                    shift.write(line)
            utm.close()
            shift.close()

            run_once = True
