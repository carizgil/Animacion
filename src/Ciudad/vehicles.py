import bpy
import random
import mathutils
import math
from math import sin
import interpola
from mathutils import Vector

def DefinirPosicionCoche(obj, ruta, tam_coche, tam_manzana, ancho_calles, altura):
    """
    Establece la posición inicial del coche en la escena y genera fotogramas clave por cada calle,
    finalizando en una posición final específica.
    """
    # Configuración inicial del coche
    velocidad = bpy.context.scene.velocidad_coche
    pos_ini = (ruta[0][0] * (tam_manzana + ancho_calles) - (ancho_calles / 2),
               ruta[0][1] * (tam_manzana + ancho_calles) - (ancho_calles / 2),
               altura)
    obj.location = pos_ini
    obj.scale = (tam_coche, tam_coche, tam_coche)
    obj.keyframe_insert(data_path="location", frame=1)

    # Animación a lo largo de la ruta
    tiempo = 1
    for k in range(1, len(ruta)):
        pos = (ruta[k][0] * (tam_manzana + ancho_calles) - (ancho_calles / 2),
               ruta[k][1] * (tam_manzana + ancho_calles) - (ancho_calles / 2),
               altura)
        avanzado = 0
        if(k > 1):
            #Para saber cuanto ha avanzado y poder utlizarlo al calcular el tiempo
            vector_intervalo = (abs(ruta[k][0] - ruta[k-1][0]), abs(ruta[k][1] - ruta[k-1][1]))
            if(vector_intervalo[0] >0):
                avanzado = vector_intervalo[0]
            else:
                avanzado = vector_intervalo[1]
                   
        obj.location = pos
        tiempo += ((1 / velocidad) * 24) * avanzado
        obj.keyframe_insert(data_path="location", frame=tiempo)
        
    # Configuramos el rango de la línea de tiempo y calculamos las trayectorias de movimiento
    bpy.context.scene.frame_start = 1
    bpy.context.scene.frame_end = int(tiempo)
    bpy.ops.object.paths_calculate()


def CrearCocheAnimado():
    """
    Crea una esfera animada para simular un coche que se desplaza por una calle.
    Selecciona una calle y una dirección aleatoria, y establece fotogramas clave
    para animar el movimiento de la esfera a lo largo de la calle.
    """

    # Obtiene propiedades de la escena
    calles_y = bpy.context.scene.n_calles_y
    calles_x = bpy.context.scene.n_calles_x
    tam_manzana = bpy.context.scene.tam_manzana
    ancho_calles = bpy.context.scene.ancho_calles
    alt_edificios = bpy.context.scene.alt_edificios
    num_coches = bpy.context.scene.num_coches
    n_giros = bpy.context.scene.n_giros

    for i in range(num_coches):

        tam_esfera = tam_manzana / 8
        altura = random.uniform(tam_esfera / 2, alt_edificios/2)

        bpy.ops.mesh.primitive_uv_sphere_add(radius=tam_esfera)
        coche = bpy.context.active_object
        coche.name = f"CocheAnimado_{i}"

        # Copiar propiedades de interpolación
        coche["metodo_interpolacion"] = bpy.context.scene.metodo_interpolacion

        if bpy.context.scene.metodo_interpolacion == "HERMITE":
            coche["velocidad_hermite"] = bpy.context.scene.velocidad_hermite
        elif bpy.context.scene.metodo_interpolacion == "CATMULL_ROM":
            coche["tension"] = bpy.context.scene.tension

        coche["oscilacion_aleatoria"] = bpy.context.scene.oscilacion_aleatoria

        if bpy.context.scene.oscilacion_aleatoria:
            coche["amplitud_oscilacion"] = bpy.context.scene.amplitud_oscilacion
            coche["frecuencia_oscilacion"] = bpy.context.scene.frecuencia_oscilacion

        coche["control_rotacion"] = bpy.context.scene.control_rotacion
        if bpy.context.scene.control_rotacion:
            coche["eje_alineacion"] = bpy.context.scene.eje_alineacion
            coche["eje_lateral"] = bpy.context.scene.eje_lateral
            coche["utilizar_alabeo"] = bpy.context.scene.utilizar_alabeo
            if bpy.context.scene.utilizar_alabeo:
                coche["ang_alabeo"] = bpy.context.scene.ang_alabeo

        """
        coche["ruta_obj"] = bpy.context.scene.ruta_obj
        ruta_obj = bpy.path.abspath(bpy.context.scene.ruta_obj)
        if os.path.exists(ruta_obj):
            bpy.ops.wm.obj_import(filepath=ruta_obj)
            coche = bpy.context.active_object
        """

        # Asignar driver a la posición y rotación del coche
        for i in range(3):
            asigna_driver_posicion(coche, i)

        for i in range(4):
            coche.rotation_mode = 'QUATERNION'
            asigna_driver_rotacion(coche, i)
        
        # Generar una ruta aleatoria con giros
        ruta = crea_ruta(n_giros, max(calles_x, calles_y))

        # Establece la posición inicial de la esfera y genera los fotogramas clave
        DefinirPosicionCoche(coche, ruta, tam_esfera, tam_manzana, ancho_calles, altura)

def crea_ruta(ngiros: int, calles: int):
    """
    Crea una ruta aleatoria de nturns giros en una cuadrícula de NxN.

    Args:
    nturns (int): Número de giros en la ruta.
    N (int): Número total de calles
    """
    # Listado de calles a elegir
    calles_set = set(range(calles + 1))

    i = 0
    j = 0
    posns = []
    # Elegimos al azar si la primera posición es en fila o columna
    fila = random.choice([True, False])
    for turn in range(ngiros + 1):
        if fila:
            fila = False
            # Elección aleatoria de la siguiente calle
            i = random.choice(list(calles_set - {i}))
        else:
            fila = True
            # Elección aleatoria de la siguiente calle
            j = random.choice(list(calles_set - {j}))
        posns.append([i, j])

    # Forzamos que acabe en la última calle
    if fila:
        i = calles
    else:
        j = calles

    posns.append([i, j])

    return posns


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

    cx = obj.animation_data.action.fcurves.find('location', index=coord)
    keyframes = cx.keyframe_points

    method = bpy.context.scene.metodo_interpolacion
    print(f"Usando método de interpolación: {method}")

    i = 0
    while i < len(keyframes) and keyframes[i].co[0] < frm:
        i += 1

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
            v1 = velocidad[i].co[1]
            pos = interpola.hermite(frm, keyframes[i-1].co[0], keyframes[i].co[0], keyframes[i-1].co[1], keyframes[i].co[1], v0, v1)

    elif method == "CATMULL_ROM":
        tension = bpy.context.scene.tension
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

    if not bpy.context.scene.oscilacion_aleatoria:
        return pos
    
    frecuencia = bpy.context.scene.frecuencia_oscilacion

    amplitud = bpy.context.scene.amplitud_oscilacion

    pos = amplitud * sin(frecuencia * frm)

    return pos