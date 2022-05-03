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
segmentation_semaphor = [2]
extraction_semaphor = [2]
dummy_semaphore = [1]
interaction_style = [0]

# input content
textures = []
label_coordinates = []
label_names = []

# testing
plotted_arc = []

colored_labels = []

shapefiles = []

colors = ['blue', 'green', 'red', 'yellow', 'purple']
