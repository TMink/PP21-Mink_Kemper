# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
import app_functions.global_shift as gs
import app_functions.obj_to_ply as otp
import app_functions.mesh_downsample as dm
import app_window.pyvista_ui as ui


if __name__ == '__main__':

    # perform global shift on content in utm_data and saves it in shift_corrds/ibj_format
    gs.utm_to_shift()

    # converts content of shift_coords/obj_format from .obj to .ply and saves it in shift_coords/ply_format
    otp.oby_to_ply()

    # decimates the meshes in shift_coords/ply_format and saves them in shift_coords/ply_format/decimated
    dm.decimate_meshes()

    # loads all converted meshes and corresponding textures in decimated_meshes and textures
    ui.get_data()

    # rotates the content of decimated_meshes at an 50 degree angle around the z-axis
    ui.transform_downsampled_meshes()

    # starts the app
    ui.colonia_4d()

