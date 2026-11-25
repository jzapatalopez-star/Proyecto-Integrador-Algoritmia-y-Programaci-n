"""
Cada linea del radicado mide exactamente 120 caracteres:
1 caracter de borde + 118 de contenido + 1 caracter de borde,
muestra N/A si no hay dirección.
"""

ANCHO = 120
INTERIOR = ANCHO - 2
NOMBRE_SISTEMA = "SIPA"


def linea_borde(caracter):
    """
    Crea una linea de borde de 120 caracteres.
    """
    return "+" + caracter * INTERIOR + "+"


def linea_centrada(texto):
    """
    Crea una linea con el texto centrado dentro del marco.
    """
    texto = texto[:INTERIOR]
    espacios = INTERIOR - len(texto)
    izquierda = espacios // 2
    derecha = espacios - izquierda
    return "|" + " " * izquierda + texto + " " * derecha + "|"


def linea_campo(etiqueta, valor):
    """
    Crea una linea 'Etiqueta.....: valor' alineada a la izquierda
    """
    puntos = "." * (30 - len(etiqueta))
    texto = "  " + etiqueta + puntos + ": " + str(valor)
    texto = texto[:INTERIOR]
    return "|" + texto + " " * (INTERIOR - len(texto)) + "|"


def numero_radicado(registro):
    """
    Retorna el ID con prefijo y ceros, por ejemplo QUE-000007
    """
    prefijos = {"Petición": "PET", "Queja": "QUE",
                "Reclamo": "REC", "Sugerencia": "SUG"}
    numero = str(registro["id"])
    numero = "0" * (6 - len(numero)) + numero
    return prefijos[registro["tipo_solicitud"]] + "-" + numero


def generar_radicado(r):
    """
    Construye el radicado completo de una PQRS.

      Radicado completo (lineas separadas por saltos de linea).
    """
    direccion = r["direccion"]
    if direccion == "":
        direccion = "N/A"
    telefono = r["telefono_contacto"] + " (" + r["tipo_telefono"] + ")"
    documento = r["tipo_documento"] + " " + r["numero_documento"]

    lineas = [
        linea_borde("="),
        linea_centrada(NOMBRE_SISTEMA + " - GESTION DE PQRS"),
        linea_centrada("Movimiento Estudiantil de Perritos y Gaticos"),
        linea_centrada("COMPROBANTE DE RADICACION"),
        linea_borde("="),
        linea_centrada("DATOS DEL RADICADO"),
        linea_borde("-"),
        linea_campo("Número de radicado", numero_radicado(r)),
        linea_campo("Fecha de radicación", r["fecha_radicacion"]),
        linea_campo("Fecha/hora de registro", r["fecha_registro"]),
        linea_campo("Estado", r["estado_peticion"]),
        linea_campo("Fecha máxima de respuesta",
                    r["fecha_maxima_respuesta"]),
        linea_borde("-"),
        linea_centrada("DATOS DEL SOLICITANTE"),
        linea_borde("-"),
        linea_campo("Nombre completo", r["nombre_completo"]),
        linea_campo("Documento", documento),
        linea_campo("Teléfono", telefono),
        linea_campo("Correo electrónico", r["correo_electronico"]),
        linea_campo("Dirección", direccion),
        linea_borde("-"),
        linea_centrada("CLASIFICACION"),
        linea_borde("-"),
        linea_campo("Tipo de solicitud", r["tipo_solicitud"]),
        linea_campo("Canal de recepción", r["canal_recepcion"]),
        linea_campo("Tipo de mascota", r["tipo_mascota"]),
        linea_campo("Campus", r["campus_relacionado"]),
        linea_borde("-"),
        linea_centrada("RESUMEN"),
        linea_borde("-"),
        linea_campo("Asunto", r["asunto_titulo"]),
        linea_borde("="),
    ]
    return "\n".join(lineas)
