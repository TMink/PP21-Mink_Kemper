# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Creates a GeoTiff from geospatial-raster-Data and .tiff-image

-1- Creates the GeoTiff image and saves it in GEOTIFF_PATH
-1.1- Search for new .tiff-image
-1.2- Combine all Data to create GeoTiff
-2- Connect the right axis. A different perspective can mean different position of axis
-3- Get the rest of the utm-cords and connect them to the shift cords
"""
# ---------------------------------------------------------------------------
import subprocess

from app_functions.general.search_for_format import search_for_format
from data.dictionarys import geotiff_bounds
from data.lists import camera_view

TIFF_PATH = 'resources/screenshots/tiff/'
GEOTIFF_PATH = 'resources/screenshots/geotiff/'
COORDS_PATH = 'database/utm_coords/'


# -1-
def do():
    # -1.1-
    tiff_list = search_for_format(TIFF_PATH, ['.tiff'], cut=True)
    geotiff_list = search_for_format(GEOTIFF_PATH, ['.tiff'], cut=True)

    tiff = [elem for elem in tiff_list if elem not in geotiff_list]

    # -1.2-
    try:
        utm_rest = utm_cords()

        # shift-cords to utm-cords
        ytop = geotiff_bounds['top'] + utm_rest['top_bottom']
        ybottom = geotiff_bounds['bottom'] + utm_rest['top_bottom']
        xleft = geotiff_bounds['left'] + utm_rest['left_right']
        xright = geotiff_bounds['right'] + utm_rest['left_right']

        # EPSG: 4326 (WGS 84 -- WGS84 - World Geodetic System 1984)
        subprocess.call(
            f'gdal_translate -of GTiff -a_srs EPSG:4326 -a_ullr '
            f'{xleft} {ytop} {xright} {ybottom} '
            f'{TIFF_PATH + tiff[0] + ".tiff"} {GEOTIFF_PATH + tiff[0] + ".tiff"}')
    except IndexError:
        print('empty list')


# -2-
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
    return cords


# -3-
def utm_cords():
    cords_list = search_for_format(COORDS_PATH, ['txt'], cut=False)

    try:
        with open(COORDS_PATH + '/' + cords_list[0], 'r') as file:
            lines = file.readlines()
            lines_list = lines[0].split(' ')
            x_coords = lines_list[3]
            y_coords = lines_list[4]
        return directions_specific(x=float(x_coords), y=float(y_coords))
    except IndexError:
        return 'empty list'
