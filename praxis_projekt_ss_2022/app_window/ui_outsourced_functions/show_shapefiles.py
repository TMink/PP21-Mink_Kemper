# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Clips the mesh with the selected polygons, normal and invert, and loads the clipped shapefiles and the clipped mesh into
the plot.
"""
# ---------------------------------------------------------------------------
from pyacvd import Clustering

from data.dictionarys import shapefiles_selected_for_clipping, original_layers, all_subdivided_layers, \
    shapefiles_clipped_layers, shapefiles_layers, shapefiles_colors, shapefiles_clipped_and_subdivided_layers


def do(self):

    self.plotter.remove_actor(shapefiles_layers.keys())
    shapefiles_layers.clear()

    # some point cloud-meshes are non-manifold. To evade this Problem, all 'excavation-side'-meshes will be
    # clustered, then subdivided and changed back into its previous mesh-form
    for key, value in original_layers.items():
        mesh_cluster = Clustering(value)
        mesh_cluster.subdivide(1)
        mesh_cluster.cluster(value.number_of_cells)
        remesh = mesh_cluster.create_mesh()
        all_subdivided_layers[key] = remesh

    for shapefile_name, shapefile_value in shapefiles_selected_for_clipping.items():
        extruded = shapefile_value.extrude((0, 0, 0.01), capping=True)
        for idx, (subdivided_layer_key, subdivided_layer_value) in enumerate(all_subdivided_layers.items()):
            clipped_shapefiles = subdivided_layer_value.clip_surface(extruded, invert=False, progress_bar=True)
            clipped_mesh = subdivided_layer_value.clip_surface(extruded, invert=True, progress_bar=True)
            shapefiles_clipped_layers[f'{shapefile_name}:{idx}'] = clipped_shapefiles
            all_subdivided_layers[subdivided_layer_key] = clipped_mesh

    for key, value in zip(shapefiles_clipped_layers.keys(), shapefiles_clipped_layers.values()):
        name = key[:key.rfind(':')]
        new_name = name[:name.rfind('_')]
        shapefiles_clipped_and_subdivided_layers[key] = self.plotter.add_mesh(mesh=value, name=key,
                                                                              color=shapefiles_colors[new_name])

    for key, value in all_subdivided_layers.items():
        shapefiles_clipped_and_subdivided_layers[key] = self.plotter.add_mesh(mesh=value, name=key, color='white')




