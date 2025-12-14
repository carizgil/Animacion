import bpy
import delete_objects
import city
import vehicles
from importlib import reload
import vehicles

reload(delete_objects)
reload(city)
reload(vehicles)

class ProceduralCityPanel(bpy.types.Panel):
    """
    Clase que define el panel de control de la ciudad en Blender.
    """
    bl_label = "Procedural City"
    bl_idname = "OBJECT_PT_ProceduralCity"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Procedural City'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        obj = context.object

        # Configuración de calles y manzanas
        row = layout.row()
        row.label(text="Creación del suelo", icon='WORLD_DATA')
        row = layout.row()
        row.prop(scene, "n_calles_x")
        row.prop(scene, "n_calles_y")
        row = layout.row()
        row.prop(scene, "tam_manzana")
        row.prop(scene, "ancho_calles")

        # Configuración de edificios
        row = layout.row()
        row.label(text="Creación de los edificios", icon='HOME')
        row = layout.row()
        row.prop(scene, "alt_edificios")
        row.prop(scene, "var_edificios")

        # Configuración de vehículos
        row = layout.row()
        row.label(text="Creación de los coches", icon='WORLD_DATA')
        row = layout.row()
        row.prop(scene, "velocidad_coche")
        row = layout.row()
        row.prop(scene, "num_coches")
        row.prop(scene, "n_giros") 

        row = layout.row()
        row.prop(scene, "oscilacion_aleatoria", text = "Oscilación aleatoria")
        if scene.oscilacion_aleatoria:
            row = layout.row()
            row.prop(scene, "amplitud_oscilacion", text = "Amplitud oscilación")
            row.prop(scene, "frecuencia_oscilacion", text = "Frecuencia oscilación") 

        # Configuración de la rotación
        row = layout.row()
        row.label(text="Rotación de los coches", icon='WORLD_DATA')
        row = layout.row()
        row.prop(scene, "control_rotacion", text="Control de la rotación")
        row = layout.row()
        if scene.control_rotacion:
            row = layout.row()
            row.prop(scene, "eje_alineacion", text="Eje de alineación")
            row = layout.row()
            row.prop(scene, "eje_lateral", text="Eje lateral")
            row = layout.row()
            row.prop(scene, "utilizar_alabeo", text="Ángulo de alabeo")
            if scene.utilizar_alabeo:
                row = layout.row()
                row.prop(scene, "ang_alabeo", text="Ángulo de alabeo")
            row = layout.row()

        # Configuración de la interpolación
        row = layout.row()
        row.label(text="Interpolación de trayectorias", icon='WORLD_DATA')
        row = layout.row()
        row.prop(scene, "metodo_interpolacion", text="Método de interpolación")
        row = layout.row()
        if scene.metodo_interpolacion == "HERMITE":
            row = layout.row()
            row.prop(scene, "velocidad_hermite", text = "Velocidad")
        elif scene.metodo_interpolacion == "CATMULL_ROM":
            row = layout.row()
            row.prop(scene, "tension", text = "Tensión")   

        # Botones para crear y borrar la ciudad
        row = layout.row()
        row.operator("object.crear_ciudad", text="Crear Ciudad")
        row = layout.row()
        row.operator("object.borrar_coches", text="Borrar Coches")
        row.operator("object.crear_coches", text="Crear Coches")



class CrearCiudadOperator(bpy.types.Operator):
    '''
    Clase que define el operador para crear la ciudad en Blender.
    '''
    bl_idname = "object.crear_ciudad"
    bl_label = "Crear Ciudad"

    def execute(self, context):
        delete_objects.delete_all(bpy.data.objects)

        city.CrearCiudad()
        
        return {'FINISHED'}
    
class OBJECT_OT_borrar_coches(bpy.types.Operator):
    """
    Clase que define el operador para borrar todos los coches de la escena.
    """
    bl_idname = "object.borrar_coches"
    bl_label = "Borrar Coches"

    def execute(self, context):
        """
        Método que se ejecuta al llamar al operador.
        """
        for obj in bpy.data.objects:
            if obj.name.startswith("CocheAnimado_"):
                bpy.data.objects.remove(obj, do_unlink=True)
        
        return {'FINISHED'}
    
class OBJECT_OT_crear_coches(bpy.types.Operator):
    """
    Operador para crear múltiples coches animados en Blender.
    """
    bl_idname = "object.crear_coches"
    bl_label = "Crear Coches Animados"
    
    def execute(self, context):
        """
        Método que se ejecuta cuando el operador es llamado.
        
        Parámetros:
        context: El contexto en el que se ejecuta el operador.
        
        Retorna:
        dict: Un diccionario indicando que el operador ha terminado con éxito.
        """
        vehicles.CrearCocheAnimado()
        
        return {'FINISHED'}
    
def register():
    
    """
    Función para registrar clases y propiedades personalizadas en Blender.
    """
    bpy.types.Scene.n_calles_x = bpy.props.IntProperty(name="n_calles_x",
                                                       description="Calles en x",
                                                       min=1,
                                                       default=5)

    bpy.types.Scene.n_calles_y = bpy.props.IntProperty(name="n_calles_y",
                                                       description="Calles en y",
                                                       min=1,
                                                       default=5)

    bpy.types.Scene.tam_manzana = bpy.props.FloatProperty(name="tam_manzana",
                                                          description="Tamaño de la manzana (L)",                                                            
                                                          min=1,
                                                          default=2)

    bpy.types.Scene.ancho_calles = bpy.props.FloatProperty(name="ancho_calles",
                                                           description="Anchura de las calles (w)",
                                                           min=0,
                                                           default=4)
    
    bpy.types.Scene.alt_edificios = bpy.props.FloatProperty(name="alt_edificios",
                                                            description="Altura promedio edificios",
                                                            min=1,
                                                            default=5)
    
    bpy.types.Scene.var_edificios = bpy.props.FloatProperty(name="var_edificios",
                                                            description="Varianza altura edificios",
                                                            min=0,
                                                            default=2)
    
    bpy.types.Scene.velocidad_coche = bpy.props.FloatProperty(name="velocidad_coche",
                                                              description="Velocidad del coche en calles por segundo",
                                                              min=0.1,
                                                              default=1.0)
    
    bpy.types.Scene.num_coches = bpy.props.IntProperty(name="num_coches",
                                                         description="Número de coches",
                                                         min=1,
                                                         max = 20,
                                                         default=2)
    
    bpy.types.Scene.n_giros = bpy.props.IntProperty(name="n_giros",
                                                    description="Número de giros",
                                                    min=0,
                                                    max=10,
                                                    default=2)
    
    bpy.types.Scene.tension = bpy.props.FloatProperty(name = "tension",
                                                        description = "Tau",
                                                        min = 0.0,
                                                        max = 1.0,
                                                        default = 0.5)
    
    bpy.types.Scene.velocidad_hermite = bpy.props.FloatVectorProperty(name = "velocidad_hermite",
                                                                    description = "Velocidad",
                                                                    subtype = 'XYZ',
                                                                    size = 3,
                                                                    default = (0.0, 0.0, 0.0))
    
    bpy.types.Scene.metodo_interpolacion = bpy.props.EnumProperty(
        name="metodo_interpolacion",
        description="Selecciona el método de interpolación",
        items=[
            ("LINEAL", "Lineal", "Interpolación lineal"),
        ("HERMITE", "Hermite", "Interpolación Hermite"),
        ("CATMULL_ROM", "Catmull-Rom", "Interpolación Catmull-Rom")
        ]
    )

    bpy.app.driver_namespace['get_pos'] = vehicles.get_posicion
    bpy.app.driver_namespace['get_quaternion'] = vehicles.get_quaternion

    bpy.types.Scene.oscilacion_aleatoria = bpy.props.BoolProperty(name="oscilacion_aleatoria",
                                                                    description="Oscilación aleatoria",
                                                                    default=False)
    
    bpy.types.Scene.amplitud_oscilacion = bpy.props.FloatProperty(name="amplitud_oscilacion",
                                                                description="Amplitud oscilación",
                                                                min=0.0,
                                                                max = 10.0,
                                                                default=0.5)
    
    bpy.types.Scene.frecuencia_oscilacion = bpy.props.FloatProperty(name="frecuencia_oscilacion",
                                                                description="Frecuencia oscilación",
                                                                min=0.0,
                                                                max = 10.0,
                                                                default=0.5)  
    
    bpy.types.Scene.control_rotacion = bpy.props.BoolProperty(name="control_rotacion",
                                                            description="Control de la rotación",
                                                            default=False)
    
    bpy.types.Scene.eje_alineacion = bpy.props.EnumProperty(
        name="eje_alineacion",
        description="Eje de alineación",
        items=[
            ("X", "X", "Eje X"),
            ("Y", "Y", "Eje Y"),
            ("Z", "Z", "Eje Z"),
            ("-X", "-X", "Eje -X"),
            ("-Y", "-Y", "Eje -Y"),
            ("-Z", "-Z", "Eje -Z")
        ]
    )

    bpy.types.Scene.eje_lateral = bpy.props.EnumProperty(
        name="eje_lateral",
        description="Eje lateral",
        items=[
            ("X", "X", "Eje X"),
            ("Y", "Y", "Eje Y"),
            ("Z", "Z", "Eje Z"),
            ("-X", "-X", "Eje -X"),
            ("-Y", "-Y", "Eje -Y"),
            ("-Z", "-Z", "Eje -Z")
        ]
    )

    bpy.types.Scene.utilizar_alabeo = bpy.props.BoolProperty(name="utilizar_alabeo",
                                                            description="Utilizar alabeo",
                                                            default=False)
    
    bpy.types.Scene.ang_alabeo = bpy.props.FloatProperty(name="ang_alabeo",
                                                        description="Ángulo de alabeo",
                                                        min=0.0,
                                                        max=360.0,
                                                        default=0.0)
    
    bpy.types.Scene.ruta_obj = bpy.props.StringProperty(name="ruta_obj",
                                                        description="Ruta del archivo OBJ",
                                                        default="",
                                                        subtype='FILE_PATH')
    

    bpy.utils.register_class(ProceduralCityPanel)
    bpy.utils.register_class(CrearCiudadOperator)
    bpy.utils.register_class(OBJECT_OT_borrar_coches)
    bpy.utils.register_class(OBJECT_OT_crear_coches)
    

def unregister():
    """
    Función para desregistrar clases y propiedades en Blender.
    """
    bpy.utils.unregister_class(ProceduralCityPanel)
    bpy.utils.unregister_class(CrearCiudadOperator)
    bpy.utils.unregister_class(OBJECT_OT_borrar_coches)
    bpy.utils.unregister_class(OBJECT_OT_crear_coches)

    del bpy.types.Scene.n_calles_x
    del bpy.types.Scene.n_calles_y
    del bpy.types.Scene.tam_manzana
    del bpy.types.Scene.ancho_calles
    del bpy.types.Scene.alt_edificios
    del bpy.types.Scene.var_edificios
    del bpy.types.Scene.velocidad_coche
    del bpy.types.Scene.num_coches
    del bpy.types.Scene.n_giros
    del bpy.types.Scene.tension
    del bpy.types.Scene.velocidad_hermite
    del bpy.types.Scene.metodo_interpolacion
    del bpy.app.driver_namespace['get_pos']
    del bpy.app.driver_namespace['get_quaternion']
    del bpy.types.Scene.oscilacion_aleatoria
    del bpy.types.Scene.amplitud_oscilacion
    del bpy.types.Scene.frecuencia_oscilacion
    del bpy.types.Scene.control_rotacion
    del bpy.types.Scene.eje_alineacion
    del bpy.types.Scene.eje_lateral
    del bpy.types.Scene.utilizar_alabeo
    del bpy.types.Scene.ang_alabeo
    del bpy.types.Scene.ruta_obj
    
if __name__ == "__main__":
    register()
