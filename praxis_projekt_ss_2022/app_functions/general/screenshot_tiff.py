# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Creates a second plot(off-screen) of the currently used meshes and takes the screenshot in the chosen resolution
"""
# ---------------------------------------------------------------------------
import pyvista as pv
from datetime import datetime
from data.dictionarys import original_layers, segmentation_extraction_clipped_layers, shapefiles_clipped_layers, \
    geotiff_bounds, geotiff_new
from data.lists import textures, colors, camera_view

# set plotter background to 'transparent'
pv.global_theme.transparent_background = True
pv.rcParams['transparent_background'] = True

# create an off-screen plotter
plotter = pv.Plotter(off_screen=True)


# creates a second plot and takes a screenshot(.tiff)
def do(tool_name: str, tex_col: str, res: list, res_name: str):
    plotter.window_size = res
    plotter.add_mesh(mesh=list(original_layers.values())[0], name='dummy', opacity=0.0, show_scalar_bar=False)

    plotter.remove_actor(original_layers.keys())
    plotter.remove_actor(segmentation_extraction_clipped_layers.keys())
    plotter.remove_actor(shapefiles_clipped_layers.keys())

    # Add the currently used meshes to plot
    if tool_name == 'excavation_layers':
        if tex_col == 'tex':
            for idx, (mesh_name, mesh_data, tex) in enumerate(zip(original_layers.keys(), original_layers.values(),
                                                                  textures)):
                plotter.add_mesh(mesh=mesh_data, name=mesh_name, texture=tex, label=mesh_name)
        if tex_col == 'col':
            for idx, (mesh_name, mesh_data, color) in enumerate(zip(original_layers.keys(),
                                                                    original_layers.values(), colors)):
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

    tiff_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    tiff_name = f'tiff_image_{tiff_datetime}_{res_name}_{camera_view[0]}.tiff'

    geotiff_new['geotiff'] = tiff_name

    plotter.screenshot(filename=
                       f'resources/screenshots/tiff/{tiff_name}',
                       transparent_background=True)


# Get the position sequence for clipped_frustum.bounds and change camera settings to match main plot. The 'res'-sequence
# depends on the perspective in which the camera views the object.
def get_position_sequence():
    if camera_view[0] == 'top':
        res = [0, 1, 2, 3]
        plotter.view_vector((0, 0, 1))
        plotter.camera.roll = -90
        plotter.enable_parallel_projection()

    elif camera_view[0] == 'bottom':
        res = [1, 0, 2, 3]
        plotter.view_yx()
        plotter.camera.roll = 270.0
        plotter.enable_parallel_projection()

    elif camera_view[0] == 'left':
        res = [5, 4, 0, 1]
        plotter.view_vector((0, -1, 0))
        plotter.enable_parallel_projection()

    elif camera_view[0] == 'right':
        res = [5, 4, 1, 0]
        plotter.view_vector((0, 1, 0))
        plotter.enable_parallel_projection()

    elif camera_view[0] == 'front':
        res = [5, 4, 2, 3]
        plotter.view_vector((1, 0, 0))
        plotter.enable_parallel_projection()

    elif camera_view[0] == 'back':
        res = [5, 4, 3, 2]
        plotter.view_vector((-1, 0, 0))
        plotter.enable_parallel_projection()

    else:
        res = []
    return res


# Depending of the perspective the frustum needs to be cut invert or not
def invert_clip():
    if camera_view[0] == 'top' or camera_view[0] == 'left' or camera_view[0] == 'front':
        res = True
    else:
        res = False
    return res


# Create a clipped frustum, take the cords of the bounds and write them in the correct sequence into geotiff_bounds
def change_camera():
    position_sequence = get_position_sequence()
    frustum = plotter.camera.view_frustum(1.77757088447)

    plane = pv.Plane(center=[0, 0, 0], i_size=50, j_size=50)

    if camera_view != 'isometric' and original_layers:
        if camera_view[0] == 'top' or camera_view[0] == 'bottom':
            plane.rotate_z(90, inplace=True)
        if camera_view[0] == 'left' or camera_view[0] == 'right':
            plane.rotate_y(90, inplace=True)
            plane.rotate_z(90, inplace=True)
        if camera_view[0] == 'back' or camera_view[0] == 'front':
            plane.rotate_y(90, inplace=True)
    plane.translate(list(original_layers.values())[0].center, inplace=True)

    clipped_frustum = frustum.clip_surface(plane, invert=invert_clip())

    geotiff_bounds['top'] = clipped_frustum.bounds[position_sequence[0]]
    geotiff_bounds['bottom'] = clipped_frustum.bounds[position_sequence[1]]
    geotiff_bounds['left'] = clipped_frustum.bounds[position_sequence[2]]
    geotiff_bounds['right'] = clipped_frustum.bounds[position_sequence[3]]
