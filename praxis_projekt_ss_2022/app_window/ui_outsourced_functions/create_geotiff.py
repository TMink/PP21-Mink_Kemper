# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Creates a GeoTiff
"""
# ---------------------------------------------------------------------------
import rasterio.plot

from app_functions.change_format import tiff_to_geotiff
from app_functions.general import screenshot_tiff
from data.dictionarys import excavation_layers, segmentation_extraction_layers, shapefiles_layers, geotiff_new
from data.lists import camera_view


def do(self, res: list, res_name: str):
    tool_name = '_'
    tex_col = '_'
    if excavation_layers:
        tool_name = 'excavation_layers'
        if self.excavation_side_texture.isChecked():
            tex_col = 'tex'
        elif self.excavation_side_color.isChecked():
            tex_col = 'col'
    elif segmentation_extraction_layers:
        tool_name = 'segmentation_extraction_tool'
        if self.segmentation_tool_texture.isChecked() or self.extraction_tool_texture.isChecked():
            tex_col = 'tex'
        elif self.segmentation_tool_color.isChecked() or self.extraction_tool_color.isChecked():
            tex_col = 'col'
    elif shapefiles_layers:
        tool_name = 'shapefiles_layers'
        if self.shapefile_tool_texture.isChecked():
            tex_col = 'tex'
        elif self.shapefile_tool_color.isChecked():
            tex_col = 'col'

    if camera_view[0] != 'isometric':
        screenshot_tiff.do(tool_name=tool_name, tex_col=tex_col, res=res, res_name=res_name)

        tiff_to_geotiff.do()

        data_name = f'resources/screenshots/geotiff/{geotiff_new["geotiff"]}'
        tiff = rasterio.open(data_name)
        rasterio.plot.show(tiff)
