# ----------------------------------------------------------------------------
# Created By  : Tobias Mink, Marvin Kemper
# ---------------------------------------------------------------------------
"""
Creates a new interaction object in plot
"""
# ---------------------------------------------------------------------------
from data.dictionarys import interaction_objects, interaction_objects_plotted, interaction_objects_loaded
from data.lists import button_selected


def do(self):
    for interaction_object_name, interaction_object_data in interaction_objects.items():
        if button_selected[0] == interaction_object_name:
            duplicates = 0
            if interaction_objects_plotted:
                # Compares the name of the object which is about to be created with the names of objects which
                # already exists and safes the length of the resulting list in 'duplicates'
                duplicates = len([val for key, val in interaction_objects_plotted.items() if
                                  interaction_object_name == key[:key.rfind('_')]])
            mesh = interaction_object_data.copy(deep=True)
            interaction_objects_plotted[f'{interaction_object_name}_{duplicates}'] = self.plotter.add_mesh(
                mesh=mesh, name=f'{interaction_object_name}_{duplicates}', )
            interaction_objects_loaded[f'{interaction_object_name}_{duplicates}'] = mesh
