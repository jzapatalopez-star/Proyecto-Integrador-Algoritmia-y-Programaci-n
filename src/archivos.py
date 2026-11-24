"""
Modulo de manejo de archivos planos del gestor de PQRS (RF-01, RF-06).

Cada tipo de solicitud se guarda en su propio archivo dentro de data/:
Peticion.txt, Queja.txt, Reclamo.txt y Sugerencia.txt.
"""

import os

# Ruta de la carpeta data/ (esta al lado de la carpeta src/)
archivo_actual = __file__                         # "src/archivos.py"
ruta_completa = os.path.abspath(archivo_actual)
CARPETA_SRC = os.path.dirname(ruta_completa)
CARPETA_DATA = os.path.join(os.path.dirname(CARPETA_SRC), "data")

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


def registro_a_linea(registro):
    """
    Convierte una PQRS (diccionario) en una linea de texto.

    Separa los datos con | y cambia los | y saltos de linea que
    escriba el usuario, para no dañar el archivo.
    """
    valores = []
    for campo in CAMPOS:
        valor = str(registro[campo])
        valor = valor.replace("|", "/").replace("\n", " ")
        valores.append(valor)
    return "|".join(valores) + "\n"


def linea_a_registro(linea):
    """Convierte una linea del archivo en una PQRS (diccionario)."""
    valores = linea[:-1].split("|")   # [:-1] quita el salto final
    registro = {}
    for i in range(len(CAMPOS)):
        registro[CAMPOS[i]] = valores[i]
    registro["id"] = int(registro["id"])
    return registro


def leer_registros(tipo_solicitud):
    """
    Lee todas las PQRS de un archivo.

    Retorna una lista de diccionarios, o una lista vacia si el
    archivo no existe.
    """
    ruta = ruta_archivo(tipo_solicitud)
    registros = []
    if os.path.exists(ruta):
        with open(ruta, "r") as archivo_txt:
            for linea in archivo_txt:
                if linea != "\n":
                    registros.append(linea_a_registro(linea))
        return registros
    else:
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

    Retorna el ID mayor mas uno.
    """
    mayor = 0
    for registro in leer_registros(tipo_solicitud):
        if registro["id"] > mayor:
            mayor = registro["id"]
    return mayor + 1


def guardar_registro(registro):
    """Agrega una PQRS nueva al final de su archivo."""
    os.makedirs(CARPETA_DATA, exist_ok=True)
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
    os.makedirs(CARPETA_DATA, exist_ok=True)
    ruta = os.path.join(CARPETA_DATA, nombre_archivo)
    with open(ruta, "w") as archivo_txt:
        archivo_txt.write(contenido)
    return ruta
