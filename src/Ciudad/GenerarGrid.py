# Autores: Carlos Izquierdo, Ianis Bacula, Luis Planella
# version ='1.0'
# --------------------------------------------------------------------------------------
""" Script que contiene el código para generar el suelo de la ciudad. """
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------

import bpy
import bmesh
import math

def altura(x, y):
    '''
    Función que calcula la altura de un punto en función de sus coordenadas x e y.

    Args:
        x (float): Coordenada x del punto.
        y (float): Coordenada y del punto.
    
    Returns:
        float: Altura del punto.
    '''
    a = 0.02
    return math.sin(x*y*a)

def generar_suelo(centro_x, centro_y):
    '''
    Función que genera el suelo de la ciudad. Se crea una malla de 100x100 con 10 subdivisiones
    en cada eje. Se modifica la altura de los vértices de la malla de forma aleatoria.

    Args:
        centro_x (float): Coordenada x del centro de la ciudad.
        centro_y (float): Coordenada y del centro de la ciudad.
    
    Returns:
        None
    '''
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()

    print("Generando suelo")

    bpy.ops.mesh.primitive_grid_add(
                                    x_subdivisions=10,
                                    y_subdivisions=10,
                                    size=100,
                                    location=(centro_x, centro_y, 0)
                                    )    

    #Cogemos el objeto activo
    obj = bpy.context.active_object

    #Creamos un ojbeto de tipo Mesh y cargamos los datos
    bm = bmesh.new()
    bm.from_mesh(obj.data)

    #Modificamos la altura de los vértices (coordenada z) de forma aleatoria en un rango de +-0.1 unidades
    for v in bm.verts:
        v.co.z = altura(v.co.x, v.co.y)

    #Actualizamos la malla
    bm.to_mesh(obj.data)
    bm.free() #Liberamos la memoria