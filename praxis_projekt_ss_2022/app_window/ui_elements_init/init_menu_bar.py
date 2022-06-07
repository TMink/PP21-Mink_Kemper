# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from PyQt5.QtGui import QFont

FONT_NAME = 'helvetiker regular'


def do(self):

    # *** Menu Bar ***
    self.main_menu.setStyleSheet(open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))
    self.main_menu.setMinimumHeight(40)
    self.main_menu.setFont(QFont(FONT_NAME, 13))

    # ** File **
    self.file_menu.setFont(QFont(FONT_NAME, 10))

    # * Exit button *
    self.exit_button.setShortcut('Ctrl+Q')
    self.exit_button.triggered.connect(self.close)
    self.file_menu.addAction(self.exit_button)

    # ** Tools **
    self.tools_menu.setFont(QFont(FONT_NAME, 10))

    # * Excavation side *
    self.excavation_side_menu.setStyleSheet(
        open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

    self.excavation_side_texture.setStatusTip('With textures')
    self.excavation_side_texture.setChecked(False)
    self.excavation_side_texture.triggered.connect(self.load_excavation_side)

    self.excavation_side_color.setStatusTip('With color')
    self.excavation_side_color.setChecked(False)
    self.excavation_side_color.triggered.connect(self.load_excavation_side)

    self.excavation_side_menu.addAction(self.excavation_side_texture)
    self.excavation_side_menu.addAction(self.excavation_side_color)
    self.tools_menu.addMenu(self.excavation_side_menu)

    # * Segmentation tool *
    self.segmentation_tool_menu.setStyleSheet(
        open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

    self.segmentation_tool_texture.setStatusTip('With textures')
    self.segmentation_tool_texture.setChecked(False)
    self.segmentation_tool_texture.triggered.connect(self.load_segmentation_tool)

    self.segmentation_tool_color.setStatusTip('With color')
    self.segmentation_tool_color.setChecked(False)
    self.segmentation_tool_color.triggered.connect(self.load_segmentation_tool)

    self.segmentation_tool_menu.addAction(self.segmentation_tool_texture)
    self.segmentation_tool_menu.addAction(self.segmentation_tool_color)
    self.tools_menu.addMenu(self.segmentation_tool_menu)

    # * Extraction tool *
    self.extraction_tool_menu.setStyleSheet(
        open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

    self.extraction_tool_texture.setStatusTip('With textures')
    self.extraction_tool_texture.setChecked(False)
    self.extraction_tool_texture.triggered.connect(self.load_extraction_tool)

    self.extraction_tool_color.setStatusTip('With color')
    self.extraction_tool_color.setChecked(False)
    self.extraction_tool_color.triggered.connect(self.load_extraction_tool)

    self.extraction_tool_menu.addAction(self.extraction_tool_texture)
    self.extraction_tool_menu.addAction(self.extraction_tool_color)
    self.tools_menu.addMenu(self.extraction_tool_menu)

    # * Shapefile tool *
    self.shapefile_menu.setStyleSheet(
        open('resources/style_sheets/main_menu_style_sheet.txt').read().replace('\n', ''))

    self.shapefile_tool_load.setStatusTip('Load shapefiles')
    self.shapefile_tool_load.setChecked(False)
    self.shapefile_tool_load.triggered.connect(self.load_shapefile_tool)

    self.shapefile_tool_info_panel.setStatusTip('Show/Hide info panel')
    self.shapefile_tool_info_panel.setChecked(False)
    self.shapefile_tool_info_panel.triggered.connect(self.sf_info_panel_hide_show)

    self.shapefile_menu.addAction(self.shapefile_tool_load)
    self.shapefile_menu.addAction(self.shapefile_tool_info_panel)
    self.tools_menu.addMenu(self.shapefile_menu)

    # ** Interaction Object/-s **
    self.interaction_objects_menu.setFont(QFont(FONT_NAME, 10))

    # * show/hide object/-s *
    self.interaction_objects_show_hide.setStatusTip('Load found/-s')
    self.interaction_objects_show_hide.setChecked(False)
    # self.objects.triggered.connect(TODO: add function name)

    # * Info panel *
    self.interaction_objects_info_panel.setStatusTip('Show/Hide info panel')
    self.interaction_objects_info_panel.setChecked(False)
    self.interaction_objects_info_panel.triggered.connect(self.io_info_panel_hide_show)

    self.interaction_objects_menu.addAction(self.interaction_objects_show_hide)
    self.interaction_objects_menu.addAction(self.interaction_objects_info_panel)

    # ** Founds **
    self.founds_menu.setFont(QFont(FONT_NAME, 10))

    # * shows/hide found/-s *
    self.founds_show_hide.setStatusTip('Load Labels')
    self.founds_show_hide.setChecked(False)
    self.founds_show_hide.triggered.connect(self.build_founds)

    # * Info panel *
    self.founds_info_panel.setStatusTip('Show/Hide info panel')
    self.founds_info_panel.setChecked(False)
    self.founds_info_panel.triggered.connect(self.f_info_panel_hide_show)

    self.founds_menu.addAction(self.founds_show_hide)
    self.founds_menu.addAction(self.founds_info_panel)

    # ** GeoTiff Screenshot **
    self.geotiff_menu.setFont(QFont(FONT_NAME, 10))

    # * 1920_1080(Full HD) *
    self.geotiff_1920_1080.triggered.connect(self.take_screenshot_1920_1080)
    self.geotiff_menu.addAction(self.geotiff_1920_1080)

    # * 3840_2160(4k) *
    self.geotiff_3840_2160.triggered.connect(self.take_screenshot_3840_2160)
    self.geotiff_menu.addAction(self.geotiff_3840_2160)

    # * 7680_4320(8k) *
    self.geotiff_7680_4320.triggered.connect(self.take_screenshot_7680_4320)
    self.geotiff_menu.addAction(self.geotiff_7680_4320)

    # * 15360_8640(16k) *
    self.geotiff_15360_8640.triggered.connect(self.take_screenshot_15360_8640)
    self.geotiff_menu.addAction(self.geotiff_15360_8640)

