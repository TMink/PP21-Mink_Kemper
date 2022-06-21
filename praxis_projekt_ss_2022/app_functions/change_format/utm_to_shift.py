# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Converts the cords of a mesh from UTM to Shift
"""
# ---------------------------------------------------------------------------
import shutil

from app_functions.general.search_for_format import search_for_format


def do(utm_path: str, shift_path: str):
    global utm, shift
    run_once = True
    decimal_places = 6

    # Get all files (.obj, .jpg, .mtl) from utm_path and shift_path
    utm_obj_list = search_for_format(utm_path, ['obj'], cut=True)
    utm_rest_list = search_for_format(utm_path, ['jpg', 'mtl'], cut=False)
    shift_obj_list = search_for_format(shift_path, ['obj'], cut=True)
    shift_rest_list = search_for_format(shift_path, ['jpg', 'mtl'], cut=False)

    # Looks if files are already present in vtk_path
    new_obj = [elem for elem in utm_obj_list if elem not in shift_obj_list]
    new_rest = [elem for elem in utm_rest_list if elem not in shift_rest_list]

    if new_obj and new_rest:

        # Copy all non .obj files into ply_path
        for elem in new_rest:
            try:
                shutil.copyfile(utm_path + elem, shift_path + elem)
            except OSError:
                print(f'cannot copy {elem} from {utm_path} to {shift_path}')

        # Execute a global shift on every .obj, save the rest of utm-cords inside a .txt-file and save the new .obj in
        # shp_path
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
