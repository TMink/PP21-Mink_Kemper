import app_functions.global_shift as gs
import app_functions.obj_to_ply as otp
import app_window.pyvista_ui as ui


if __name__ == '__main__':
    gs.utm_to_shift()
    otp.obj_ply_convert()
    ui.get_data()
    ui.transform_downsampled_meshes()
    ui.colonia_4d()

