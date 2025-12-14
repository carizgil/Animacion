# Autores: Carlos Izquierdo, Ianis Bacula, Luis Planella
# version ='1.0'
# --------------------------------------------------------------------------------------
""" Script que contiene el código para generar los edificios de nuestra ciudad. """
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------

import random
import bpy

def CrearCubo(location_x, location_y, location_z, l, h):
    '''
    Función que genera un edificio en nuestra ciudad. Para generar un edificio utilizamos un 
    cubo sobre el que aplicamos la posición y tamaño calculados según las opciones seleccionadas
    en la interfaz.

    Args:
        location_x (float): Posición en el eje x del edificio.
        location_y (float): Posición en el eje y del edificio.
        location_z (float): Posición en el eje z del edificio.
        l (float): Tamaño de los lados del edificio.
        h (float): Altura del edificio.
    
    Returns:
        None
    '''
    # Creación del edificio
    bpy.ops.mesh.primitive_cube_add(
        size=2,
        enter_editmode=False,
        align='WORLD',
        location=(location_x, location_y, location_z),
        scale=(l/2, l/2, h/2)
    )
    obj = bpy.context.active_object
    obj.name = "Building"
    obj.location.z = h / 2
    
    '''
    # Coge el objeto activo y le añade una keyframe en el frame 1
    obj.location = (location_x, location_y, 50)
    obj = bpy.context.active_object
    obj.keyframe_insert(data_path="location", frame=1)

    # Modifica la posición del objeto en el frame 20 y le añade una keyframe cambiando la altura
    obj.location.z = h / 2
    obj.keyframe_insert(data_path="location", frame=20)
     '''
     
def CrearCiudad():
    '''
    Función para crear una ciudad en Blender. Esta función obitene los valores de las
    variables de la interfaz.
    Mediante un bucle anidado se crean los edificios en la ciudad. Para cada edificio se
    calcula su altura en función de la altura base y la variabilidad seleccionada en la interfaz.
    Se llama a la función CrearCubo para crear el edificio.

    Args:
        None
    
    Returns:
        None
    '''
    # Asignación de variables desde la interfaz
    Nx = bpy.context.scene.n_calles_x
    Ny = bpy.context.scene.n_calles_y
    l = bpy.context.scene.tam_manzana
    w = bpy.context.scene.ancho_calles
    h_base = bpy.context.scene.alt_edificios  # Altura base de los edificios
    variabilidad = bpy.context.scene.var_edificios  # Variabilidad de la altura
    
    # Posición del cursor como punto de inicio
    p = bpy.context.scene.cursor.location
    
    pos_x = p[0] + l/2
    pos_y = p[1] + l/2

    for i in range(Nx + 1):
        for j in range(Ny + 1):
            # Modifica la altura de cada edificio en función de la variabilidad
            h = h_base + random.uniform(-variabilidad, variabilidad)

            pos_z = p[2] + h - 1

            # Crear el cubo (edificio) con la altura modificada
            CrearCubo(pos_x, pos_y, pos_z, l, h)

            pos_y += l + w
        
        pos_y = l / 2
        pos_x += l + w
