# Autores: Carlos Izquierdo, Ianis Bacula, Luis Planella
# version ='2.0'
# --------------------------------------------------------------------------------
""" 
Script que contiene el código que implementa las funciones para calcular la
posición y rotación de los objetos de la ciudad
"""
# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------
import bpy
import os
import interpola
from mathutils import Vector
import mathutils
import math
from math import sin

def get_posicion(frm: float, obj, coord: int):
    """
    Calcula la posición del objeto en el fotograma dado, utilizando
    el algoritmo de interpolación implementado.
    Args:
    - frm (float): El fotograma actual.
    - obj (Object): El objeto que sigue la trayectoria.
    - coord (int): La coordenada de la posición a calcular.
    Returns:
    - float: La posición del objeto en la coordenada especificada.
    """
    
    # Si no existe la curva velocidad_hermite, usa un valor predeterminado
    vx = obj.animation_data.action.fcurves.find('velocidad_hermite', index=coord)
    if vx is not None:
        velocidad = vx.keyframe_points
    else:
        velocidad = []
    # Comprobación para que solo se ejecute la función si está activada la reparametrización
    if obj.utilizar:
        if obj.animation_data and obj.animation_data.action:
            frm =  change_frame(obj, frm)
    
    cx = obj.animation_data.action.fcurves.find('location', index=coord)
    keyframes = cx.keyframe_points
    
    i = 0
    while i < len(keyframes) and keyframes[i].co[0] < frm:
        i += 1
        
    method = obj.metodo_interpolacion

    if method == "LINEAL":
        if i == 0:
            pos = keyframes[0].co[1]
        elif i == len(keyframes):
            pos = keyframes[-1].co[1]
        else:
            pos = interpola.lineal(frm, keyframes[i-1].co[0], keyframes[i].co[0], keyframes[i-1].co[1], keyframes[i].co[1])

    elif method == "HERMITE":
        if i == 0:
            pos = keyframes[0].co[1]
        elif i == len(keyframes):
            pos = keyframes[-1].co[1]
        else:
            v0 = velocidad[i-1].co[0]
            v1 = velocidad[i].co[0]
            pos = interpola.hermite(frm, keyframes[i-1].co[0], keyframes[i].co[0], keyframes[i-1].co[1], keyframes[i].co[1], v0, v1)

    elif method == "CATMULL_ROM":
        tension = obj.tension
        # Si solo hay dos keyframes
        if len(keyframes) == 2:
            if i<=0:
                # Caso 1: El fotograma deseado esta antes que el primer fotograma clave y se toma la posición del primer fotograma clave
                pos = keyframes[0].co[1]
            elif i>=len(keyframes):
                # Caso 2: El fotograma deseado esta después del ultimo fotograma clave y se toma la posición del último fotograma clave
                pos = keyframes[i-1].co[1]
            else:
                pos = interpola.catmull_rom(frm, keyframes[i-1].co[0], keyframes[i].co[0], tension, keyframes[i-1].co[1], keyframes[i-1].co[1], keyframes[i].co[1], keyframes[i].co[1])
        else:
            if i <= 0:
                # Caso 1: El fotograma deseado esta antes que el primer fotograma clave y se toma la posición del primer fotograma clave
                pos = keyframes[0].co[1]
            # Caso 2: El fotograma deseado esta después del ultimo fotograma clave y se toma la posición del último fotograma clave
            elif i >= len(keyframes):
                pos = keyframes[i-1].co[1]
            elif i <2:
                pos = interpola.catmull_rom(frm, keyframes[i-1].co[0], keyframes[i].co[0], tension, keyframes[i-1].co[1], keyframes[i-1].co[1], keyframes[i].co[1], keyframes[i+1].co[1])
            elif i > len(keyframes)-3:
                pos = interpola.catmull_rom(frm, keyframes[i-1].co[0], keyframes[i].co[0], tension, keyframes[i-2].co[1], keyframes[i-1].co[1], keyframes[i].co[1], keyframes[i].co[1])
            else:
                pos = interpola.catmull_rom(frm, keyframes[i-1].co[0], keyframes[i].co[0], tension, keyframes[i-2].co[1], keyframes[i-1].co[1], keyframes[i].co[1], keyframes[i+1].co[1])
    
    if coord == 2:  # Aplicar oscilación solo en el eje Z
       pos += aplicar_oscilacion(obj, pos, frm)
    return pos
            
def get_quat_from_vecs(e, t):
    """
    Calcula el cuaternión que representa la rotación entre dos vectores.
    
    Parámetros:
    e (Vector): Eje de alineacion del objeto.
    t (Vector): Vector tangente del objeto.
    
    Retorna:
    Quaternion: El cuaternión que representa la rotación entre los dos vectores.
    """
    e = Vector(e)
    t = Vector(t)

    v = e.cross(t)
    v.normalize()
    angle = math.acos(max(-1.0, min(1.0, e.dot(t))))

    angulo_def = angle / 2

    sen = math.sin(angulo_def)
    cos = math.cos(angulo_def)

    q = mathutils.Quaternion((cos, sen*v.x, sen*v.y, sen*v.z))

    return q

def get_quaternion(frm: float, obj, coord: int):
    """
    Calcula el cuaternión de rotación del objeto en el fotograma dado determinando
    un vector con las posiciones actual y anterior del objeto y otro vector con la
    dirección tangente
    Parámetros:
    - frame (float): El fotograma actual.
    - obj (Object): El objeto que sigue la trayectoria.
    - coord (int): La coordenada del cuaternión a calcular.
    
    Retorna:
    - float: El cuaternión de rotación del objeto en la coordenada especificada.
    """
    
    # Obtener la posición actual y anterior del objeto
    if frm == bpy.context.scene.frame_start:
        v1 = mathutils.Vector([get_posicion(frm+1, obj, 0), get_posicion(frm+1, obj, 1), get_posicion(frm+1, obj, 2)])
        v0 = mathutils.Vector([get_posicion(frm, obj, 0), get_posicion(frm, obj, 1), get_posicion(frm, obj, 2)])
    else:
        v1 = mathutils.Vector([get_posicion(frm, obj, 0), get_posicion(frm, obj, 1), get_posicion(frm, obj, 2)])
        v0 = mathutils.Vector([get_posicion(frm-1, obj, 0), get_posicion(frm-1, obj, 1), get_posicion(frm-1, obj, 2)])

    # Vector tangente a la trayectoria
    d = v1 - v0
    t = d.normalized()

    # Seleccionar el eje inicial del objeto basado en la propiedad 'alinear_eje'
    if obj.eje_alineacion == 'X':
        e1 = Vector((1, 0, 0))
    elif obj.eje_alineacion == 'Y':
        e1 = Vector((0, 1, 0))
    elif obj.eje_alineacion == 'Z':
        e1 = Vector((0, 0, 1))
    elif obj.eje_alineacion == '-X':
        e1 = Vector((-1, 0, 0))
    elif obj.eje_alineacion == '-Y':
        e1 = Vector((0, -1, 0))
    elif obj.eje_alineacion == '-Z':
        e1 = Vector((0, 0, -1))

    if obj.eje_lateral == 'X':
        e2 = Vector((1, 0, 0))
    elif obj.eje_lateral == 'Y':
        e2 = Vector((0, 1, 0))
    elif obj.eje_lateral == 'Z':
        e2 = Vector((0, 0, 1))
    elif obj.eje_lateral == '-X':
        e2 = Vector((-1, 0, 0))
    elif obj.eje_lateral == '-Y':
        e2 = Vector((0, -1, 0))
    elif obj.eje_lateral == '-Z':
        e2 = Vector((0, 0, -1))

    l = obtener_vec_lateral(t)
    up = t.cross(l)
    up.normalize()

    # Alinear con el tangente
    q1 = get_quat_from_vecs(e1, t)

    # Ajustar de la direcció vertical
    e3 = e1.cross(e2)
    e3prima = q1 @ e3

    q2 = get_quat_from_vecs(e3prima, -up)
    qFinal = q2 @ q1

    
    #Aplicacion de una rotacion adicional
    if obj.utilizar_alabeo == True:
        AngleAdicional = math.radians(obj.ang_alabeo)
        ang_def = AngleAdicional / 2
        sen = math.sin(ang_def)
        cos = math.cos(ang_def)
        q3 = mathutils.Quaternion((cos, sen*t.x, sen*t.y, sen*t.z))
        qFinal = q3 @ qFinal


    return qFinal[coord]

def obtener_vec_lateral(v):
    """
    Calcula el vector lateral del objeto determinando un vector con 
    la dirección tangente deseada.

    Parámetros:
    - v (Vector): Vector tangente del objeto.
    
    Retorna:
    - l (Vector): El vector lateral del objeto en el frame deseadp.
    """
    z = mathutils.Vector((0, 0, 1))

    l = z.cross(v)
    l.normalize()
    return l

def aplicar_oscilacion(obj, pos, frm):
    """
    Aplica una oscilación aleatoria al objeto en la posición dada.

    Parámetros:
    - obj (Object): El objeto al que se le aplica la oscilación.
    - pos (float): La posición actual del objeto en la coordenada especificada.
    - frm (float): El fotograma actual.
    - coord (int): La coordenada de la posición a modificar (0: X, 1: Y, 2: Z).

    Retorna:
    - float: La posición del objeto con la oscilación aplicada.
    """

    if not obj.oscilacion_aleatoria:
        return pos
    
    frecuencia = obj.frecuencia_oscilacion

    amplitud = obj.amplitud_oscilacion

    pos = amplitud * sin(frecuencia * frm)
    return pos

class OBJECT_PT_driver_panel(bpy.types.Panel):
    """
    Panel de control para el operador de asignación de drivers de posición.
    """
    bl_label = "Panel de Drivers"
    bl_idname = "OBJECT_PT_driver_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        """
        Método para dibujar el panel.
        
        Parámetros:
        context: El contexto en el que se dibuja el panel.
        """
        layout = self.layout
        obj = context.active_object
        
        layout.prop(obj, "metodo_interpolacion", text = "Algortimo")

        if obj.metodo_interpolacion == "CATMULL_ROM":
            layout.prop(obj, "tension", text = "Tensión")
        elif obj.metodo_interpolacion == "HERMITE":
            layout.prop(obj, "velocidad_hermite", text = "Velocidad")
        
        layout.prop(obj, "oscilacion_aleatoria", text = "Oscilación aleatoria")
        if obj.oscilacion_aleatoria:
            layout.prop(obj, "amplitud_oscilacion", text = "Amplitud de la oscilación")
            layout.prop(obj, "frecuencia_oscilacion", text = "Frecuencia de la oscilación")
        
        layout.prop(obj, "control_rotacion", text = "Control de rotación")
        if obj.control_rotacion == True:
            layout.prop(obj, "eje_alineacion", text = "Eje de alineación")
            layout.prop(obj, "eje_lateral", text = "Eje Lateral")
            layout.prop(obj, "utilizar_alabeo", text = "Utilizar Alabeo")
            if obj.utilizar_alabeo == True:
                layout.prop(obj, "ang_alabeo", text = "Ángulo de Alabeo")

        layout.prop(obj, "ruta_obj", text="Ruta del archivo OBJ")
        
        layout.prop(obj, "utilizar", text="Utilizar reparametrización")
        if obj.utilizar:
            layout.prop(obj, "dist_deseada", text="Distancia deseada")
            
        layout.operator("object.asigna_driver")

# Clase del operador para establecer los drivers al objeto
class OBJECT_OT_asigna_driver_posicion(bpy.types.Operator):
    """
    Operador para asignar drivers de posición a un objeto en Blender.
    """
    bl_idname = "object.asigna_driver"
    bl_label = "Asigna Driver Posición"
    
    def execute(self, context):
        """
        Método que se ejecuta cuando el operador es llamado.
        
        Parámetros:
        context: El contexto en el que se ejecuta el operador.
        event: El evento que desencadena la invocación del operador.
        
        Retorna:
        dict: Un diccionario indicando que el operador ha terminado con éxito.
        """
        
        obj = context.active_object 
        ruta_absoluta = bpy.path.abspath(obj.ruta_obj)
        print(ruta_absoluta)
        if os.path.exists(ruta_absoluta):
            print("El archivo existe")
            bpy.ops.wm.obj_import(filepath=ruta_absoluta)
            # Eliminamos el cubo o cualquier objeto que se haya importado
            bpy.data.objects.remove(bpy.data.objects['Cube'])
            obj = context.active_object
            
        if obj.utilizar:
            longitud_recorrida(obj)
            
            """
            obj.dist_deseada = 0
            obj.keyframe_insert(data_path="dist_deseada", frame=bpy.context.scene.frame_start)
            obj.dist_deseada = obj.dist_recorrida
            obj.keyframe_insert(data_path="dist_deseada", frame=bpy.context.scene.frame_end)
            """
            
        for i in range(3):
            asigna_driver_posicion(obj, i)
        
        if obj.control_rotacion == True:
            obj.rotation_mode = 'QUATERNION'
            for i in range(4):
                asigna_driver_rotacion(obj, i)
            
        return {'FINISHED'}
    
def asigna_driver_posicion(obj,coord):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('location',coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_pos(frame, self, {coord})"

def asigna_driver_rotacion(obj,coord):
    # Creamos el driver en la coordenada elegida. El driver se queda
    # guardado en la variable drv
    drv = obj.driver_add('rotation_quaternion',coord).driver
    # Habilitamos la posibilidad de que reciba el propio objeto, que
    # necesitaremos para acceder a los fotogramas clave.
    drv.use_self = True
    # Asignamos la expresión que queremos que se utilice.
    # Se está utilizando una "f-string" para constuir una cadena
    # a partir del valor de las variables coord y method
    drv.expression = f"get_quaternion(frame, self, {coord})"
    
def longitud_recorrida(obj):
    """
    Calcula y registra la distancia recorrida por un objeto en cada frame como una propiedad animada.

    Parámetros:
    obj: Objeto de Blender con una trayectoria definida.

    Returns:
    No devuelve valores. Registra la distancia recorrida (`dist_recorrida`) como keyframes.
    """
    # a falso
    distancia = 0
    obj.dist_recorrida = distancia
    obj.keyframe_insert(data_path="dist_recorrida", frame = 0)

    for i in range(1, bpy.context.scene.frame_end + 1):
        p = mathutils.Vector([get_posicion(i, obj, j) - get_posicion(i-1, obj, j) for j in range(3)])
        distancia += p.length
        obj.dist_recorrida = distancia
        obj.keyframe_insert(data_path="dist_recorrida", frame = i)
    #a verdadero
def change_frame(obj, frame):
    fc = obj.animation_data.action.fcurves.find('dist_deseada')
    if fc is not None:
        long = obj.dist_deseada
    else: 
        long = fc.evaluate(frame)
    
    frm = frame_desde_longitud(obj, long)
    return frm


def frame_desde_longitud(obj, long):
    """
    Encuentra el frame que corresponde a una distancia recorrida deseada, interpolando si es necesario.

    Parámetros:
    obj: Objeto de Blender.

    Returns:
    Devuelve el frame correspondiente a la distancia deseada.
    """

    curva_recorrida = obj.animation_data.action.fcurves.find('dist_recorrida')
    iterador = 0
    while (iterador < len(curva_recorrida.keyframe_points) and curva_recorrida.keyframe_points[iterador].co[1] < long):
        iterador += 1
            
    if iterador < len(curva_recorrida.keyframe_points):
        frm = interpola.lineal(long, curva_recorrida.keyframe_points[iterador-1].co[0], curva_recorrida.keyframe_points[iterador].co[0], curva_recorrida.keyframe_points[iterador-1].co[1], curva_recorrida.keyframe_points[iterador].co[1])
    else:
        frm = curva_recorrida.keyframe_points[-1].co[0]

    return frm

def register():
    """
    Registra el operador en Blender y añade la función get_posicion al namespace de drivers.
    """
    bpy.types.Object.tension = bpy.props.FloatProperty(name = "tension",
                                                        description = "Tau",
                                                        min = 0.0,
                                                        max = 1.0,
                                                        default = 0.5)
    
    bpy.types.Object.velocidad_hermite = bpy.props.FloatVectorProperty(name = "velocidad_hermite",
                                                                    description = "Velocidad",
                                                                    subtype = 'XYZ',
                                                                    size = 3,
                                                                    default = (0.0, 0.0, 0.0))
    
    bpy.types.Object.metodo_interpolacion = bpy.props.EnumProperty(
        name="metodo_interpolacion",
        description="Selecciona el método de interpolación",
        items=[
            ("LINEAL", "Lineal", "Interpolación lineal"),
        ("HERMITE", "Hermite", "Interpolación Hermite"),
        ("CATMULL_ROM", "Catmull-Rom", "Interpolación Catmull-Rom")
        ]
    )
    
    bpy.types.Object.oscilacion_aleatoria = bpy.props.BoolProperty(
        name="oscilacion_aleatoria",
        description="Oscilación aleatoria",
        default=False
    )

    bpy.types.Object.amplitud_oscilacion = bpy.props.FloatProperty(
        name="amplitud_oscilacion",
        description="Amplitud de la oscilación",
        min=0.0,
        max=5.0,
        default = 1.0
    )
    

    bpy.types.Object.frecuencia_oscilacion = bpy.props.FloatProperty(
        name="frecuencia_oscilacion",
        description="Frecuencia de la oscilación",
        min=0.0,
        max=5.0,
        default=1.0
    )
    

    bpy.types.Object.eje_alineacion = bpy.props.EnumProperty(
        name="eje_alineacion",
        description="Eje Alineacion",
        items=[
            ("X", "X", "Eje X"),
            ("Y", "Y", "Eje Y"),
            ("Z", "Z", "Eje Z"),
            ("-X", "-X", "Eje -X"),
            ("-Y", "-Y", "Eje -Y"),
            ("-Z", "-Z", "Eje -Z")
        ]
    )

    bpy.types.Object.eje_lateral = bpy.props.EnumProperty(
        name="eje_lateral",
        description="Eje Lateral",
        items=[
            ("X", "X", "Eje X"),
            ("Y", "Y", "Eje Y"),
            ("Z", "Z", "Eje Z"),
            ("-X", "-X", "Eje -X"),
            ("-Y", "-Y", "Eje -Y"),
            ("-Z", "-Z", "Eje -Z")
        ]
    )

    bpy.types.Object.utilizar_alabeo = bpy.props.BoolProperty(
        name="utilizar_alabeo",
        description="Utilizar Alabeo",
        default=False
    )

    bpy.types.Object.ang_alabeo = bpy.props.FloatProperty(  
        name="ang_alabeo",
        description="Ángulo de Alabeo",
        default=0.0,
        min=0.0,
        max=360.0
    )

    bpy.types.Object.control_rotacion = bpy.props.BoolProperty(
        name="control_rotacion",
        description="Activar/Desactivar control de rotación",
        default=True
    )
    
    bpy.types.Object.ruta_obj = bpy.props.StringProperty(
    name="Ruta del archivo",
    description="Selecciona un archivo OBJ",
    default="",
    subtype='FILE_PATH'
    )
    
    bpy.types.Object.utilizar = bpy.props.BoolProperty(name = "Utilizar",
                                                       description="Utilizar la reparametrizacion",
                                                    default = False)

    bpy.types.Object.dist_deseada = bpy.props.FloatProperty(name = "Distancia deseada",
                                                    description="Distancia deseada para la reparametrizacion", 
                                                    default = 0)
                                                    
    bpy.types.Object.dist_recorrida = bpy.props.FloatProperty(name = "Distancia recorrida",
                                                    description="Distancia recorrida con interpolación")
                                                    

    bpy.utils.register_class(OBJECT_OT_asigna_driver_posicion)
    bpy.utils.register_class(OBJECT_PT_driver_panel)
    
    bpy.app.driver_namespace['get_pos'] = get_posicion
    bpy.app.driver_namespace['get_quaternion'] = get_quaternion

def unregister():
    """
    Desregistra el operador en Blender y elimina la función get_posicion del namespace de drivers.
    """
    bpy.utils.unregister_class(OBJECT_OT_asigna_driver_posicion)
    bpy.utils.unregister_class(OBJECT_PT_driver_panel)
    
    del bpy.app.driver_namespace['get_pos']
    del bpy.app.driver_namespace['get_quaternion']
    del bpy.types.Scene.metodo_interpolacion
    del bpy.types.Scene.velocidad_hermite
    del bpy.types.Scene.tension
    
    del bpy.types.Object.oscilacion_aleatoria
    del bpy.types.Object.amplitud_oscilacion
    del bpy.types.Object.frecuencia_oscilacion
    
    del bpy.types.Object.eje_alineacion
    del bpy.types.Object.control_rotacion
    del bpy.types.Object.eje_lateral
    del bpy.types.Object.ang_alabeo
    del bpy.types.Object.utilizar_alabeo
    del bpy.types.Object.ruta_obj
    
    del bpy.types.Object.dist_deseada
    del bpy.types.Object.dist_recorrida
    del bpy.types.Object.utilizar
    
if __name__ == "__main__":
    register()