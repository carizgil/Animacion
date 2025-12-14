# Repositorio para la asignatura Animación del Grado en Ingeniería Multimedia.
## Grupo 07
### Miembros:
- Carlos Izquierdo
- Luis Planella
- Ianis Bacula

## Instrucciones

El código de las diferentes prácticas y proyectos debe incorporarse a
este repositorio. Se deberán seguir las instrucciones que se indiquen para cada
entrega, en cuanto a la organización del repositorio en carpetas, nombres de ficheros,
etc.  

Igualmente, se indicará la forma en que debe utilizarse este documento README.md
para documentar el trabajo que se realice. En primer lugar, se deberá indicar
el número de grupo y la composición del mismo al inicio de este documento.
El documento está escrito usando el [formato Markdown](https://es.wikipedia.org/wiki/Markdown).  

No debéis añadir al repositorio ficheros binarios tales como ficheros
blend, vídeos, documentos pdf, doc, odt,... **La adición de estos
tipos de ficheros se penalizará con hasta 2 puntos de la nota del
ejercicio correspondiente.**

## Contenido del repositorio inicial

El repositorio tiene la siguiente estructura:

<pre>
doc/
  -> doc/image
    -> doc/image/LEEME_Practica1
      --> doc/image/LEEME_Practica1/ejemplo.png
      --> doc/image/LEEME_Practica1/addon.png
    -> doc/image/LEEME_Practica2
      --> doc/image/LEEME_Practica2/ejemplo.png
      --> doc/image/LEEME_Practica2/addon.png
    -> doc/image/LEEME_Practica3
      --> doc/image/LEEME_Practica3/ejemplo.png
      --> doc/image/LEEME_Practica3/interfaz.png
    -> doc/image/LEEME_Practica4
      --> doc/image/LEEME_Practica4/ejemplo.png
      --> doc/image/LEEME_Practica4/interfaz.png
  -> doc/LEEME_Practica1.md
  -> doc/LEEME_Practica2.md
  -> doc/LEEME_Practica3.md
  -> doc/LEEME_Practica4.md

src/
-> src/Ciudad/
      -> src/Ciudad/city.py
      -> src/Ciudad/delete_objects.py
      -> src/Ciudad/GenerarGrid.py
      -> src/Ciudad/interpola.py
      -> src/Ciudad/posicion.py
      -> src/Ciudad/user_interface.py
      -> src/Ciudad/vehicles.py
  -> src/Interpolacion/
      -> src/Interpolacion/interpola.py
      -> src/Interpolacion/posicion.py

README.md
</pre>

En la carpeta `src/` encontraréis dos directorios. Uno con el desarrollo de la ciudad y otro con el desarrollo de un circuito de pruebas

En la carpeta `src/Ciudad/` encontraréis los scripts relacionados con la creación de la ciudad y los vehículos, asi como la animación de estos últimos

En la carpeta `src/Ciudad/city.py` contiene las funciones necesarias y la lógica para crear la ciudad

En la carpeta `src/Ciudad/delete_objects.py` contiene la funcion para eliminar los objetos de la escena

En la carpeta `src/Ciudad/GenerarGrid.py` contiene las funciones necesarias para poder generar el suelo de la ciduad

En la carpeta `src/Ciudad/interpola.py` contiene funciones de interpolación lineal, Hermite y Catmull-Rom utilizadas en la animación de los vehículos.

En la carpeta `src/Ciudad/posicion.py` contiene la función que calcula la interpolación en cada frame además de calcular la rotación y la asignación de los drivers para las coordinadas correspondientes.

En la carpeta `src/Ciudad/user_interface.py` contiene la interfaz del usuario para que pueda poner las caracterísiticas de la ciudad que él quiera.

En la carpeta `src/Ciudad/vehicles.py` contiene las funciones necesarias y la lógica para crear la ciudad


En la carpeta `src/Interpolacion/` encontraréis los scripts relacionados con un ciruciot de pruebas para obsdervar el funcionamietno de los métodos de interpolación y el control de rotación asi como también la prueba de la oscilación

El scrpit `src/Interpolacion/interpola.py` tiene los métodos de interpolación aplicados al objeto.

El script `src/Interpolacion/posicion.py` contiene la función que calcula la interpolación en cada frame, además del código que implementa la interfaz de usuario. Por otra parte, también tiene implementada una función que calcula el cuaternión de rotación basado en vectores de alineación y tangencia para determinar la orientación del objeto.

La carpeta `doc/` la utilizaréis para crear la documentación
relacionada con el proyecto. Si necesitáis añadir figuras, cread una
carpeta `images/` dentro de la carpeta `doc/` y
añadidlas ahí. Para cada entrega debéis crear un fichero con la
documentación que se indique.

El archivo `LEEME_Practica1.md` presenta una documentación más detallada con lo referente a los algoritmos de interpolación de la práctica 1
El archivo `LEEME_Práctica2.md` presenta una documentación más detallada con lo referente a la Fase 2 donde se crea la ciudad y se implementa lo hecho en la fase 1
El archivo `LEEME_Practica3.md` presenta una documentación con los añadidos a la práctica 1. Es necesario leerse el docuemnto 'LEEME_Practica1.md' para comprender el funcionamiento completo del proyecto.
El archivo `LEEME_Practica4.md` presenta una documentación con los añadidos a la práctica 1 y la práctica 3. Es necesario leerse el docuemnto 'LEEME_Practica1.md' y 'LEEME_Practica3.md' para comprender el funcionamiento completo del proyecto.

