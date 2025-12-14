# Autores: Carlos Izquierdo, Ianis Bacula, Luis Planella
# version ='1.0'
# --------------------------------------------------------------------------------------
""" Script que contiene el código para eliminar los objetos de la ciudad. """
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------

import bpy

def delete_all(cad):
    '''
    Función que elimina todos los objetos de la ciudad.

    Args:
        cad (list): Lista con los objetos de la ciudad.
    
    Returns:
        None
    '''
    bpy.ops.object.select_all(action = 'DESELECT')
    
    for obj in cad:
        if obj.name.startswith("Building"):
            obj.select_set(True)
        
        if obj.name.startswith("Grid"):
            obj.select_set(True)

        if obj.name.startswith("CocheAnimado_"):
            obj.select_set(True)

        if obj.name.startswith("Sphere"):
            obj.select_set(True)

    bpy.ops.object.delete()
    