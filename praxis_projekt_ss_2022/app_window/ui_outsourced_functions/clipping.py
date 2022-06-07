# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
from data.dictionarys import segmentation_extraction_clipped_layers, original_layers, segmentation_extraction_layers
from data.lists import camera_vector, extraction_semaphor, segmentation_semaphor, textures, colors


def do(self, use: str, param: []):
    self.plotter.remove_actor(segmentation_extraction_clipped_layers.keys())
    segmentation_extraction_clipped_layers.clear()

    # for idx, elem in enumerate(original_layers.values()):
    for idx, elem in enumerate(original_layers.values()):
        name = "clipped_layer_%d" % idx
        if use == 'segmentation':
            camera_vector[0] = param[1]
            camera_vector[1] = param[0]
            segmentation_extraction_clipped_layers[name] = elem.clip(normal=param[0], origin=param[1],
                                                                     inplace=False)
        elif use == 'extraction':
            segmentation_extraction_clipped_layers[name] = elem.clip_box(param[0].bounds, invert=False)

    if extraction_semaphor[0] == 0 or segmentation_semaphor[0] == 0:
        for tex, name in zip(textures, segmentation_extraction_clipped_layers.keys()):
            segmentation_extraction_layers[name] = self.plotter.add_mesh(
                mesh=segmentation_extraction_clipped_layers[name], texture=tex, name=name, show_scalar_bar=False,
                reset_camera=False)
        self.build_legend(do='remove')
    elif extraction_semaphor[0] == 1 or segmentation_semaphor[0] == 1:
        for col, name in zip(colors, segmentation_extraction_clipped_layers.keys()):
            segmentation_extraction_layers[name] = self.plotter.add_mesh(
                mesh=segmentation_extraction_clipped_layers[name], color=col, name=name, show_scalar_bar=False,
                reset_camera=False)
        self.build_legend(do='add')

    # check for found/-s
    if self.founds_show_hide.isChecked():
        self.check_founds()
