# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import pyvista as pv
from datetime import datetime
from data.dictionarys import decimated_layers, segmentation_extraction_clipped_layers, shapefiles_clipped_layers, \
    geotiff_bounds
from data.lists import textures, colors, camera_vector, camera_view

pv.global_theme.transparent_background = True
pv.rcParams['transparent_background'] = True
plotter = pv.Plotter(window_size=[1920, 1080], off_screen=False) # Full-HD
# plotter = pv.Plotter(window_size=[3840, 2160], off_screen=True) # 4k
# plotter = pv.Plotter(window_size=[7680, 4320], off_screen=True) # 8k
# plotter = pv.Plotter(window_size=[15360, 8640], off_screen=False) # 16k
# plotter = pv.Plotter(window_size=[30720, 17280], off_screen=True) # 32k


# creates a second plot and takes a screenshot(.tiff)
def take_screenshot(tool_name: str, tex_col: str):
    plotter.add_mesh(mesh=list(decimated_layers.values())[0], name='dummy', opacity=0.0, show_scalar_bar=False)
    if tool_name == 'extraction_layers':
        if tex_col == 'tex':
            for idx, (mesh_name, mesh_data, tex) in enumerate(zip(decimated_layers.keys(), decimated_layers.values(),
                                                                  textures)):
                plotter.add_mesh(mesh=mesh_data, name=mesh_name, texture=tex, label=mesh_name)
        if tex_col == 'col':
            for idx, (mesh_name, mesh_data, color) in enumerate(zip(decimated_layers.keys(),
                                                                    decimated_layers.values(), colors)):
                plotter.add_mesh(mesh=mesh_data, name=mesh_name, color=color, label=mesh_name)
    if tool_name == 'segmentation_extraction_tool':
        if tex_col == 'tex':
            for tex, name in zip(textures, segmentation_extraction_clipped_layers.keys()):
                plotter.add_mesh(mesh=segmentation_extraction_clipped_layers[name], name=name, texture=tex,
                                 show_scalar_bar=False, reset_camera=False)
        if tex_col == 'col':
            for col, name in zip(colors, segmentation_extraction_clipped_layers.keys()):
                plotter.add_mesh(mesh=segmentation_extraction_clipped_layers[name], color=col, name=name,
                                 show_scalar_bar=False, reset_camera=False)
    if tool_name == 'shapefile_tool':
        if tex_col == 'tex':
            for idx, (clipped_name, clipped_data, tex) in enumerate(zip(shapefiles_clipped_layers.keys(),
                                                                        shapefiles_clipped_layers.values(),
                                                                        textures)):
                plotter.add_mesh(mesh=clipped_data, name=clipped_name, texture=tex, label=clipped_name)
        if tex_col == 'col':
            for idx, (clipped_name, clipped_data, color) in enumerate(zip(shapefiles_clipped_layers.keys(),
                                                                          shapefiles_clipped_layers.values(),
                                                                          colors)):
                plotter.add_mesh(mesh=clipped_data, name=clipped_name, color=color, label=clipped_name)

    change_camera()
    # plotter.screenshot(filename=f'resources/tif/tif_image_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.tiff',
    #                   transparent_background=True)
    #plotter.screenshot(filename=f'resources/screenshots/tiff/tif_image.tiff', transparent_background=True)
    plotter.show()


def lets_try():
    if camera_view[0] == 'top':
        res = [0, 1, 3, 2]
        plotter.view_vector((0, 0, 1))
        plotter.camera.roll = -90

    elif camera_view[0] == 'bottom':
        res = [1, 0, 3, 2]
        plotter.view_yx()
        plotter.camera.roll = 270.0

    elif camera_view[0] == 'left':
        res = [5, 4, 1, 0]
        plotter.view_vector((0, 1, 0))

    elif camera_view[0] == 'right':
        res = [5, 4, 0, 1]
        plotter.view_vector((0, -1, 0))

    elif camera_view[0] == 'front':
        res = [5, 4, 3, 2]
        plotter.view_vector((1, 0, 0))

    elif camera_view[0] == 'back':
        res = [5, 4, 2, 3]
        plotter.view_vector((-1, 0, 0))

    else:
        res = []
    return res


def lets_try_2():
    if camera_view[0] == 'top' or camera_view[0] == 'left' or camera_view[0] == 'front':
        res = True
    else:
        res = False
    return res


def change_camera():
    test = lets_try()
    # frustum = plotter.camera.view_frustum(1.664)
    frustum = plotter.camera.view_frustum(1.728)

    plane = pv.Plane(i_size=plotter.window_size[1], j_size=plotter.window_size[0])

    if camera_view != 'isometric' and decimated_layers:
        if camera_view[0] == 'top' or camera_view[0] == 'bottom':
            plane.rotate_z(90, inplace=True)
        if camera_view[0] == 'left' or camera_view[0] == 'right':
            plane.rotate_y(90, inplace=True)
            plane.rotate_z(90, inplace=True)
        if camera_view[0] == 'back' or camera_view[0] == 'front':
            plane.rotate_y(90, inplace=True)
    plane.translate(list(decimated_layers.values())[0].center, inplace=True)

    clipped_frustum = frustum.clip_surface(plane, invert=lets_try_2())

    plane_height = clipped_frustum.bounds[test[0]] - clipped_frustum.bounds[test[1]]
    plane_width = clipped_frustum.bounds[test[2]] - clipped_frustum.bounds[test[3]]

    reference_plane = pv.Plane(i_size=plane_height, j_size=plane_width)

    if camera_view != 'isometric' and decimated_layers:
        if camera_view[0] == 'bottom':
            reference_plane.rotate_y(180, inplace=True)
        if camera_view[0] == 'left' or camera_view[0] == 'right':
            reference_plane.rotate_y(90, inplace=True)
            reference_plane.rotate_z(90, inplace=True)
        if camera_view[0] == 'back' or camera_view[0] == 'front':
            reference_plane.rotate_y(90, inplace=True)
    reference_plane.translate(list(decimated_layers.values())[0].center, inplace=True)

    geotiff_bounds['top'] = reference_plane.bounds[test[0]]
    geotiff_bounds['bottom'] = reference_plane.bounds[test[1]]
    geotiff_bounds['left'] = reference_plane.bounds[test[3]]
    geotiff_bounds['right'] = reference_plane.bounds[test[2]]

    #plotter.add_mesh(mesh=frustum, color='red', style='wireframe')
    #plotter.add_mesh(mesh=plane, color='blue')
    #plotter.add_mesh(mesh=reference_plane, color='green')
