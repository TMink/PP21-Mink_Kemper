# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""  """
# ---------------------------------------------------------------------------
# lists of actor names (str)
interaction_actors = []

# lists of plotted meshes (VTK)
plotted_interaction_actors = []

# semaphores
excavation_semaphor = [2]
segmentation_semaphor = [2]
extraction_semaphor = [2]
shapefile_semaphor = [2]
dummy_semaphore = [1]
interaction_style = [0]

# input content
textures = []
found_coordinates = []
found_names = []

# testing
plotted_arc = []

colored_founds = []

volume = []

colors = ['blue', 'green', 'red', 'yellow', 'purple']

button_selected = ['_']
button_selected_for_deletion = ['_']

testing_things = [0]

clicked = [0]

clicked_tracked = [0]

clicked_somewhere_else = [0]

camera_vector = [0, 0]

camera_view = ['isometric']

center_coords = []
