# Autores: Carlos Izquierdo, Ianis Bacula, Luis Planella
# version ='1.0'
# --------------------------------------------------------------------------------------
""" Script que contiene las funciones de interpolación lineal, Hermite y Catmull-Rom """
# --------------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------------

def lineal(t: float, t0: float, t1: float, x0: float, x1: float):
    """
    Algoritmo de interpolación lineal

    Parameters
    ----------
    t : float
        tiempo entre t0 y t1 en el que queremos la posición
    t0 : float
        inicio del tramo
    t1 : float
        fin del tramo
    x0 : float
        posicion al inicio del tramo
    x1 : float
        posición al final del tramo

    Returns
    -------
    float
        El valor interpolado en el tiempo t.

    """
    u = (t - t0) / (t1 - t0) # Proporción de tiempo transcurrido
    x = x0 + u * (x1 - x0)
    return x

def hermite(t: float, t0: float, t1: float, x0: float, x1: float, v0: float, v1: float):
    """
    Algoritmo de interpolación Hermite

    Parameters
    ----------
    t : float
        tiempo entre t0 y t1 en el que queremos la posición
    t0 : float
        inicio del tramo
    t1 : float
        fin del tramo
    x0 : float
        posición al inicio del tramo
    x1 : float
        posición al final del tramo
    v0 : float
        velocidad al inicio del tramo
    v1 : float
        velocidad al final del tramo
    Returns
    -------
    float
        El valor interpolado en el tiempo t.

    """
    u = (t - t0) / (t1 - t0) # Proporción de tiempo transcurrido

    # Coeficientes de Hermite
    h00 = 2 * u**3 - 3 * u**2 + 1
    h10 = u**3 - 2 * u**2 + u
    h01 = -2 * u**3 + 3 * u**2
    h11 = u**3 - u**2

    # Interpolación Hermite
    x = x0 * h00 + x1 * h01 + v0 * h10 + v1 * h11

    return x

def catmull_rom(t: float, t0: float, t1: float, tau: float, x0: float, x1: float, x2: float, x3: float):
    """
    Algoritmo de interpolación Catmull-Rom

    Parameters
    ----------
    t : float
        tiempo entre t0 y t1 en el que queremos la posición
    t0 : float
        inicio del tramo
    t1 : float
        fin del tramo
    tau : float
        tensión de la curva
    x0 : float
        posición al inicio del tramo
    x1 : float
        posición al final del tramo anterior
    x2 : float
        posición al inicio del tramo siguiente
    x3 : float
        posición al final del tramo

    Returns
    -------
    float
        El valor interpolado en el tiempo t.

    """
    v1 = tau * (x3 - x1) 
    v0 = tau * (x2 - x0)

    x = hermite(t, t0, t1, x1, x2, v1, v0)

    return x