# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import rasterio.plot

from app_functions.change_format.tiff_to_geotiff import tiff_to_geotiff
from app_functions.screenshot_tiff import take_screenshot


def do():
    take_screenshot(tool_name='segmentation_extraction_tool', tex_col='tex')

    #tiff_to_geotiff()

    #data_name = 'resources/screenshots/geotiff/tif_image.tiff'
    #tiff = rasterio.open(data_name)
    #rasterio.plot.show(tiff)
