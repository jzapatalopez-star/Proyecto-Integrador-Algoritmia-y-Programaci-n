"""
Modulo de reportes del gestor de PQRS.

Calcula las estadisticas de las PQRS guardadas y arma un reporte de
texto con el mismo marco de 120 caracteres del radicado. Para guardarlo
en data/ se puede usar archivos.exportar_texto().
"""

from datetime import datetime

import archivos
import radicado
import validaciones as v

DIAS_ALERTA = 5


# Funciones de apoyo

def convertir_fecha(texto):
    """
    Convierte un texto 'DD/MM/AAAA' (o 'DD/MM/AAAA HH:MM') en fecha.

    Solo toma el dia, el mes y el año; la hora no se usa.
    """
    dia = int(texto[0:2])
    mes = int(texto[3:5])
    año = int(texto[6:10])
    fecha = datetime(año, mes, dia)
    return fecha


def fecha_de_hoy():
    """Retorna la fecha de hoy sin la hora."""
    ahora = datetime.now()
    hoy = datetime(ahora.year, ahora.month, ahora.day)
    return hoy


def contar_por(registros, campo, valores):
    """Cuenta cuantas PQRS hay por cada valor de un campo."""
    conteo = {}
    for valor in valores:
        conteo[valor] = 0
    for registro in registros:
        valor = registro[campo]
        conteo[valor] = conteo[valor] + 1
    return conteo


# Calculo de las estadisticas

def promedio_dias_respuesta(registros):
    """
    Estadistica obligatoria: promedio de dias para responder una PQRS.

    Cuenta los dias entre la fecha de radicacion y la fecha de
    solucion. Retorna None si no hay PQRS solucionadas.
    """
    total_dias = 0
    cantidad = 0
    for registro in registros:
        if registro["estado_peticion"] == "Solucionada":
            radicada = convertir_fecha(registro["fecha_radicacion"])
            solucion = convertir_fecha(registro["fecha_solucion"])
            diferencia = solucion - radicada
            total_dias = total_dias + diferencia.days
            cantidad = cantidad + 1
    if cantidad == 0:
        return None
    promedio = total_dias / cantidad
    promedio = int(promedio + 0.5)      # redondear al entero mas cercano
    return promedio


def resueltas_a_tiempo(registros):
    """
    Cuenta las PQRS solucionadas antes de su fecha maxima.

    Retorna una lista: [resueltas a tiempo, total de solucionadas].
    """
    a_tiempo = 0
    total = 0
    for registro in registros:
        if registro["estado_peticion"] == "Solucionada":
            total = total + 1
            solucion = convertir_fecha(registro["fecha_solucion"])
            maxima = convertir_fecha(registro["fecha_maxima_respuesta"])
            if solucion <= maxima:
                a_tiempo = a_tiempo + 1
    return [a_tiempo, total]


def buscar_activas(registros):
    """Retorna las PQRS que todavia no estan Solucionadas."""
    activas = []
    for registro in registros:
        if registro["estado_peticion"] != "Solucionada":
            activas.append(registro)
    return activas


def mas_antiguas(activas):
    """
    Busca las PQRS activas con la fecha de radicacion mas antigua.

    Retorna una lista, porque puede haber varias con la misma fecha.
    """
    if len(activas) == 0:
        return []

    # Paso 1: encontrar la fecha mas antigua
    fecha_minima = convertir_fecha(activas[0]["fecha_radicacion"])
    for registro in activas:
        fecha = convertir_fecha(registro["fecha_radicacion"])
        if fecha < fecha_minima:
            fecha_minima = fecha

    # Paso 2: guardar todas las que tienen esa fecha
    resultado = []
    for registro in activas:
        fecha = convertir_fecha(registro["fecha_radicacion"])
        if fecha == fecha_minima:
            resultado.append(registro)
    return resultado


def dias_restantes(registro, hoy):
    """Retorna cuantos dias faltan para la fecha maxima de respuesta."""
    maxima = convertir_fecha(registro["fecha_maxima_respuesta"])
    diferencia = maxima - hoy
    return diferencia.days


# Armado del reporte

def agregar_seccion(lineas, titulo):
    """Agrega a la lista el titulo de una seccion con sus bordes."""
    lineas.append(radicado.linea_borde("-"))
    lineas.append(radicado.linea_centrada(titulo))
    lineas.append(radicado.linea_borde("-"))


def generar_reporte():
    """Calcula todas las estadisticas y retorna el reporte como texto."""
    registros = archivos.leer_todos()
    activas = buscar_activas(registros)
    hoy = fecha_de_hoy()

    # Encabezado
    lineas = []
    lineas.append(radicado.linea_borde("="))
    titulo = radicado.NOMBRE_SISTEMA + " - GESTION DE PQRS"
    lineas.append(radicado.linea_centrada(titulo))
    lineas.append(radicado.linea_centrada("REPORTE ESTADISTICO"))
    lineas.append(radicado.linea_borde("="))
    lineas.append(radicado.linea_campo("Fecha del reporte",
                                       hoy.strftime("%d/%m/%Y")))
    lineas.append(radicado.linea_campo("Total de PQRS", len(registros)))

    # Estadistica obligatoria: promedio de dias de respuesta
    agregar_seccion(lineas, "TIEMPO DE RESPUESTA")
    promedio = promedio_dias_respuesta(registros)
    if promedio is None:
        texto = "Sin PQRS solucionadas"
    else:
        texto = str(promedio) + " días"
    lineas.append(radicado.linea_campo("Promedio de días de respuesta",
                                       texto))

    # Estadistica 1: cantidad por tipo de solicitud
    agregar_seccion(lineas, "CANTIDAD POR TIPO DE SOLICITUD")
    conteo = contar_por(registros, "tipo_solicitud", v.TIPOS_SOLICITUD)
    for tipo in v.TIPOS_SOLICITUD:
        lineas.append(radicado.linea_campo(tipo, conteo[tipo]))

    # Estadistica 2: cantidad por tipo de mascota
    agregar_seccion(lineas, "CANTIDAD POR TIPO DE MASCOTA")
    conteo = contar_por(registros, "tipo_mascota", v.MASCOTAS)
    for mascota in v.MASCOTAS:
        lineas.append(radicado.linea_campo(mascota, conteo[mascota]))

    # Estadistica 3: estado de las PQRS y cumplimiento del plazo
    agregar_seccion(lineas, "ESTADO Y CUMPLIMIENTO DEL PLAZO")
    conteo = contar_por(registros, "estado_peticion", v.ESTADOS)
    for estado in v.ESTADOS:
        lineas.append(radicado.linea_campo(estado, conteo[estado]))
    resultado = resueltas_a_tiempo(registros)
    a_tiempo = resultado[0]
    total = resultado[1]
    if total == 0:
        texto = "Sin PQRS solucionadas"
    else:
        porcentaje = a_tiempo * 100 / total
        porcentaje = int(porcentaje + 0.5)
        texto = (str(a_tiempo) + " de " + str(total)
                 + " (" + str(porcentaje) + "%)")
    lineas.append(radicado.linea_campo("Solucionadas dentro del plazo",
                                       texto))

    # Estadistica 4: PQRS activas mas antiguas
    agregar_seccion(lineas, "PQRS ACTIVA(S) MAS ANTIGUA(S)")
    antiguas = mas_antiguas(activas)
    if len(antiguas) == 0:
        lineas.append(radicado.linea_centrada("No hay PQRS activas"))
    for registro in antiguas:
        fecha = convertir_fecha(registro["fecha_radicacion"])
        dias = (hoy - fecha).days
        texto = (str(dias) + " días desde " + registro["fecha_radicacion"]
                 + " - " + registro["asunto_titulo"])
        numero = radicado.numero_radicado(registro)
        lineas.append(radicado.linea_campo(numero, texto))

    # Estadistica 5: PQRS por vencer y vencidas
    agregar_seccion(lineas, "POR VENCER (" + str(DIAS_ALERTA)
                    + " DIAS O MENOS) Y VENCIDAS")
    hay_alertas = False
    for registro in activas:
        dias = dias_restantes(registro, hoy)
        numero = radicado.numero_radicado(registro)
        if dias < 0:
            texto = ("Vencida hace " + str(-dias) + " días - "
                     + registro["asunto_titulo"])
            lineas.append(radicado.linea_campo(numero, texto))
            hay_alertas = True
        elif dias <= DIAS_ALERTA:
            texto = ("Vence en " + str(dias) + " días - "
                     + registro["asunto_titulo"])
            lineas.append(radicado.linea_campo(numero, texto))
            hay_alertas = True
    if not hay_alertas:
        lineas.append(radicado.linea_centrada("Ninguna"))

    lineas.append(radicado.linea_borde("="))
    return radicado.unir_lineas(lineas)
