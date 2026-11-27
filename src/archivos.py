"""
Modulo de manejo de archivos planos del gestor de PQRS (RF-01, RF-06).

Cada tipo de solicitud se guarda en su propio archivo dentro de data/:
Peticion.txt, Queja.txt, Reclamo.txt y Sugerencia.txt.
"""

import os

# Carpeta donde se guardan los archivos planos
CARPETA_DATA = "data"

# Archivo donde se guarda cada tipo de solicitud
ARCHIVOS = {
    "Petición": "Peticion.txt",
    "Queja": "Queja.txt",
    "Reclamo": "Reclamo.txt",
    "Sugerencia": "Sugerencia.txt",
}

# Orden de los campos dentro de cada linea (igual en los 4 archivos)
CAMPOS = [
    "id", "nombre_completo", "tipo_documento", "numero_documento",
    "tipo_telefono", "telefono_contacto", "correo_electronico",
    "direccion", "tipo_solicitud", "fecha_radicacion",
    "canal_recepcion", "asunto_titulo", "descripcion_detallada",
    "tipo_mascota", "campus_relacionado", "fecha_registro",
    "fecha_maxima_respuesta", "estado_peticion", "fecha_solucion",
]


def ruta_archivo(tipo_solicitud):
    """Retorna la ruta del archivo de un tipo de solicitud."""
    return os.path.join(CARPETA_DATA, ARCHIVOS[tipo_solicitud])


def crear_archivos():
    """
    Crea los 4 archivos de PQRS si todavia no existen.

    Python lo crea si no existe y,
    si ya existe, no borra lo que tiene.
    """
    for tipo in ARCHIVOS:
        with open(ruta_archivo(tipo), "a") as archivo_txt:
            archivo_txt.write("")


def limpiar_texto(texto):
    """
    Cambia los | que escriba el usuario por /, para que no se
    confundan con el separador del archivo.
    """
    nuevo = ""
    for caracter in texto:
        if caracter == "|":
            nuevo = nuevo + "/"
        else:
            nuevo = nuevo + caracter
    return nuevo


def registro_a_linea(registro):
    """Convierte una PQRS (diccionario) en una linea separada por |."""
    linea = ""
    for i in range(len(CAMPOS)):
        valor = limpiar_texto(str(registro[CAMPOS[i]]))
        if i > 0:
            linea = linea + "|"     
        linea = linea + valor
    return linea + "\n"


def separar_linea(linea):
    """Separa una linea del archivo en una lista de datos usando |."""
    valores = []
    dato = ""
    for caracter in linea:
        if caracter == "|":
            valores.append(dato)
            dato = ""
        else:
            dato = dato + caracter
    valores.append(dato)            
    return valores


def linea_a_registro(linea):
    """Convierte una linea del archivo en una PQRS (diccionario)."""
    valores = separar_linea(linea[:-1])     # [:-1] quita el salto final
    registro = {}
    for i in range(len(CAMPOS)):
        registro[CAMPOS[i]] = valores[i]
    registro["id"] = int(registro["id"])
    return registro


def leer_registros(tipo_solicitud):
    """Lee todas las PQRS de un archivo y las retorna en una lista."""
    registros = []
    with open(ruta_archivo(tipo_solicitud), "r") as archivo_txt:
        for linea in archivo_txt:
            if linea != "\n":
                registros.append(linea_a_registro(linea))
    return registros


def leer_todos():
    """Lee las PQRS de los 4 archivos y las junta en una sola lista."""
    todos = []
    for tipo in ARCHIVOS:
        for registro in leer_registros(tipo):
            todos.append(registro)
    return todos


def siguiente_id(tipo_solicitud):
    """
    Calcula el siguiente ID de un archivo (RF-01).

    Retorna el ID mayor mas uno, o 1 si el archivo esta vacio.
    """
    mayor = 0
    for registro in leer_registros(tipo_solicitud):
        if registro["id"] > mayor:
            mayor = registro["id"]
    return mayor + 1


def guardar_registro(registro):
    """Agrega una PQRS nueva al final de su archivo."""
    ruta = ruta_archivo(registro["tipo_solicitud"])
    with open(ruta, "a") as archivo_txt:
        archivo_txt.write(registro_a_linea(registro))


def buscar_registro(tipo_solicitud, id_buscado):
    """
    Busca una PQRS por su tipo e ID.

    Retorna la PQRS encontrada, o None si no existe.
    """
    for registro in leer_registros(tipo_solicitud):
        if registro["id"] == id_buscado:
            return registro
    return None


def actualizar_registro(registro_modificado):
    """
    Reemplaza una PQRS que ya existe en su archivo.

    Lee todo el archivo, cambia la PQRS con el mismo ID y vuelve a
    escribir todas las lineas.
    """
    tipo = registro_modificado["tipo_solicitud"]
    registros = leer_registros(tipo)
    with open(ruta_archivo(tipo), "w") as archivo_txt:
        for registro in registros:
            if registro["id"] == registro_modificado["id"]:
                registro = registro_modificado
            archivo_txt.write(registro_a_linea(registro))


def exportar_texto(nombre_archivo, contenido):
    """
    Guarda un texto (radicado o reporte) en la carpeta data/.

    Retorna la ruta donde quedo guardado el archivo.
    """
    ruta = os.path.join(CARPETA_DATA, nombre_archivo)
    with open(ruta, "w") as archivo_txt:
        archivo_txt.write(contenido)
    return ruta
