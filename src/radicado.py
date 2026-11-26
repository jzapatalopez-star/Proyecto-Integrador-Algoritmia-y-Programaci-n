"""
Modulo que arma en un texto un radicado.

Cada linea mide exactamente 120 caracteres: 1 de borde, 118 de
contenido y 1 de borde. Muestra N/A si no hay direccion, ya que es un campo opcional.
"""

ANCHO = 120
INTERIOR = ANCHO - 2
NOMBRE_SISTEMA = "SIPA"


def repetir(caracter, veces):
    """Retorna un texto con el caracter repetido varias veces."""
    texto = ""
    contador = 0
    while contador < veces:
        texto = texto + caracter
        contador = contador + 1
    return texto


def unir_lineas(lineas):
    """Une una lista de lineas en un solo texto, una debajo de otra."""
    texto = ""
    for i in range(len(lineas)):
        if i > 0:
            texto = texto + "\n"    # salto de linea entre una y otra
        texto = texto + lineas[i]
    return texto


def linea_borde(caracter):
    """Crea una linea de borde de 120 caracteres, ej: +-----+"""
    return "+" + repetir(caracter, INTERIOR) + "+"


def linea_centrada(texto):
    """Crea una linea con el texto centrado dentro del marco."""
    texto = texto[:INTERIOR]
    espacios = INTERIOR - len(texto)
    izquierda = espacios // 2
    derecha = espacios - izquierda
    return "|" + repetir(" ", izquierda) + texto + repetir(" ", derecha) + "|"


def linea_campo(etiqueta, valor):
    """Crea una linea 'Etiqueta.....: valor' alineada a la izquierda."""
    puntos = repetir(".", 30 - len(etiqueta))
    texto = "  " + etiqueta + puntos + ": " + str(valor)
    texto = texto[:INTERIOR]
    relleno = repetir(" ", INTERIOR - len(texto))
    return "|" + texto + relleno + "|"


def numero_radicado(registro):
    """Retorna el ID con prefijo y ceros, por ejemplo QUE-000007."""
    prefijos = {"Petición": "PET", "Queja": "QUE",
                "Reclamo": "REC", "Sugerencia": "SUG"}
    numero = str(registro["id"])
    numero = repetir("0", 6 - len(numero)) + numero
    return prefijos[registro["tipo_solicitud"]] + "-" + numero


def generar_radicado(registro):
    """Retorna el radicado completo de una PQRS como un solo texto."""
    # Si no hay direccion se muestra N/A
    direccion = registro["direccion"]
    if direccion == "":
        direccion = "N/A"

    # Telefono con su tipo, por ejemplo: 3001234567 (Celular)
    telefono = registro["telefono_contacto"]
    telefono = telefono + " (" + registro["tipo_telefono"] + ")"

    # Documento con su tipo, por ejemplo: CC 1037654321
    documento = registro["tipo_documento"]
    documento = documento + " " + registro["numero_documento"]

    lineas = [
        linea_borde("="),
        linea_centrada(NOMBRE_SISTEMA + " - GESTION DE PQRS"),
        linea_centrada("Movimiento Estudiantil de Perritos y Gaticos"),
        linea_centrada("COMPROBANTE DE RADICACION"),
        linea_borde("="),
        linea_centrada("DATOS DEL RADICADO"),
        linea_borde("-"),
        linea_campo("Número de radicado", numero_radicado(registro)),
        linea_campo("Fecha de radicación", registro["fecha_radicacion"]),
        linea_campo("Fecha/hora de registro", registro["fecha_registro"]),
        linea_campo("Estado", registro["estado_peticion"]),
        linea_campo("Fecha máxima de respuesta",
                    registro["fecha_maxima_respuesta"]),
        linea_borde("-"),
        linea_centrada("DATOS DEL SOLICITANTE"),
        linea_borde("-"),
        linea_campo("Nombre completo", registro["nombre_completo"]),
        linea_campo("Documento", documento),
        linea_campo("Teléfono", telefono),
        linea_campo("Correo electrónico", registro["correo_electronico"]),
        linea_campo("Dirección", direccion),
        linea_borde("-"),
        linea_centrada("CLASIFICACION"),
        linea_borde("-"),
        linea_campo("Tipo de solicitud", registro["tipo_solicitud"]),
        linea_campo("Canal de recepción", registro["canal_recepcion"]),
        linea_campo("Tipo de mascota", registro["tipo_mascota"]),
        linea_campo("Campus", registro["campus_relacionado"]),
        linea_borde("-"),
        linea_centrada("RESUMEN"),
        linea_borde("-"),
        linea_campo("Asunto", registro["asunto_titulo"]),
        linea_borde("="),
    ]
    return unir_lineas(lineas)
