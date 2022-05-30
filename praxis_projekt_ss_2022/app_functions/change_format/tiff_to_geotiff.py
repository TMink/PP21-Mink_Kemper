# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import subprocess

from app_functions.search_for_format import search_for_format
from data.dictionarys import geotiff_bounds
from data.lists import camera_view

TIFF_PATH = 'resources/screenshots/tiff/'
GEOTIFF_PATH = 'resources/screenshots/geotiff/'
COORDS_PATH = 'database/utm_coords/'


# creates a raster and combines it with .tiff to create a georeferenced .tiff (GeoTiff)
def tiff_to_geotiff():

    tiff = test_if_tiff()
    print(tiff)

    try:
        utm_rest = utm_cords()

        ytop = geotiff_bounds['top'] + utm_rest['top_bottom']
        ybottom = geotiff_bounds['bottom'] + utm_rest['top_bottom']
        xleft = geotiff_bounds['left'] + utm_rest['left_right']
        xright = geotiff_bounds['right'] + utm_rest['left_right']

        subprocess.call(
            f'gdal_translate -of GTiff -a_srs EPSG:4326 -a_ullr '
            f'{xleft} {ytop} {xright} {ybottom} '
            f'{TIFF_PATH + tiff[0] + ".tiff"} {GEOTIFF_PATH + tiff[0] + ".tiff"}')
    except IndexError:
        print('empty list')


def directions_specific(x: float, y: float):
    cords = {
        'top_bottom': 0.0,
        'left_right': 0.0
    }
    if camera_view[0] == 'top' or camera_view[0] == 'bottom':
        cords['top_bottom'] = x
        cords['left_right'] = y
    if camera_view[0] == 'left' or camera_view[0] == 'right':
        cords['left_right'] = x
    if camera_view[0] == 'front' or camera_view[0] == 'back':
        cords['left_right'] = y
    print(cords)
    return cords


def test_if_tiff():
    tiff_list = search_for_format(TIFF_PATH, ['.tiff'], cut=True)
    geotiff_list = search_for_format(GEOTIFF_PATH, ['.tiff'], cut=True)

    new_tiff = [elem for elem in tiff_list if elem not in geotiff_list]

    print(new_tiff)
    return new_tiff


def utm_cords():
    coords_list = search_for_format(COORDS_PATH, ['txt'], cut=False)

    try:
        with open(COORDS_PATH + '/' + coords_list[0], 'r') as file:
            lines = file.readlines()
            lines_list = lines[0].split(' ')
            x_coords = lines_list[3]
            y_coords = lines_list[4]
            print(directions_specific(x=float(x_coords), y=float(y_coords)))
        return directions_specific(x=float(x_coords), y=float(y_coords))
    except IndexError:
        return 'empty list'
