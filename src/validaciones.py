"""
Modulo de validaciones del gestor de PQRS.

Contiene las listas de valores permitidos y las funciones que revisan
si los datos escritos por el usuario son correctos (RF-02, RF-03,
RF-04 y RF-05). Cada funcion de validacion retorna True si el dato
es valido y False si no lo es.
"""

from datetime import datetime

# Caracteres para revisar los textos (nombre, documento, asunto...)
LETRAS = ("abcdefghijklmnopqrstuvwxyz"
          "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
          "áéíóúÁÉÍÓÚñÑüÜ")
DIGITOS = "0123456789"
SIGNOS_PUNTUACION = ".,;:¿?¡!()-\"'"

# Diccionario y listas con los valores permitidos
TIPOS_DOCUMENTO = {
    "Cédula de ciudadanía": "CC",
    "Tarjeta de identidad": "TI",
    "Cédula de extranjería": "CE",
    "Pasaporte": "PP",
    "NIT": "NIT",
}
TIPOS_TELEFONO = ["Celular", "Fijo", "Corporativo", "Otro"]
TIPOS_SOLICITUD = ["Petición", "Queja", "Reclamo", "Sugerencia"]
CANALES = ["Presencial", "Correo electrónico", "Página web",
           "Teléfono", "Redes sociales", "Otro"]
MASCOTAS = ["Perro", "Gato"]
CAMPUS = [
    "Campus Medellín - Ciudad Universitaria",
    "Campus Medellín - Ciudadela Robledo",
    "Campus en el Área de la salud",
    "Campus Medellín - Sede de Posgrado",
    "Campus Medellín - Edificio San Ignacio",
    "Campus Medellín - Antigua Escuela de Derecho",
    "Campus Medellín - Edificio Antioquia",
    "Campus Medellín - Casas Patrimoniales",
    "Campus Medellín - Edificio de Extensión",
]

# Estados de la PQRS, en el orden del flujo permitido
ESTADOS = ["Registrada", "En proceso", "Solucionada"]



# RF-02: Validacion de los datos del solicitante

def validar_nombre(nombre):
    """
    Permite verificar que el nombre ingresado por el usuario sea
    correcto: de 3 a 100 caracteres, solo letras (con tildes y ñ),
    espacios, apostrofes y guiones.
    """
    if len(nombre) < 3 or len(nombre) > 100:
        return False
    permitidos = LETRAS + " '-"
    for letra in nombre:
        if letra not in permitidos:
            return False
    return True


def validar_numero_documento(numero_documento):
    """
    Permite verificar que el numero de documento ingresado por el
    usuario sea correcto: solo digitos, entre 3 y 15.
    """
    if len(numero_documento) < 3 or len(numero_documento) > 15:
        return False
    for digito in numero_documento:
        if digito not in DIGITOS:
            return False
    return True


def validar_telefono(telefono):
    """
    Permite verificar que el numero telefonico ingresado por el
    usuario solo contenga digitos y que sean exactamente 10.
    """
    if len(telefono) != 10:
        return False
    for digito in telefono:
        if digito not in DIGITOS:
            return False
    return True


def validar_correo(correo):
    """
    Permite verificar que el correo ingresado por el usuario sea
    correcto: maximo 254 caracteres, sin espacios, un unico @,
    texto antes del @ y un punto dentro del dominio que no este
    ni al inicio ni al final.
    """
    if len(correo) > 254 or " " in correo:
        return False
    if correo.count("@") != 1:
        return False
    usuario, dominio = correo.split("@")
    if usuario == "" or "." not in dominio:
        return False
    if dominio[0] == "." or dominio[-1] == ".":
        return False
    return True


def validar_direccion(direccion):
    """
    Permite verificar que la direccion ingresada por el usuario sea
    correcta. Si no la ingresa es valida, por ser un campo opcional.
    Si la escribe, debe tener de 5 a 200 caracteres y solo letras,
    numeros, espacios y # - . / ,
    """
    if direccion == "":
        return True
    if len(direccion) < 5 or len(direccion) > 200:
        return False
    permitidos = LETRAS + DIGITOS + " #-./,"
    for caracter in direccion:
        if caracter not in permitidos:
            return False
    return True



# RF-03: Validacion de la informacion de la PQRS

def validar_fecha_radicacion(texto):
    """
    Permite convertir y verificar la fecha de radicacion escrita por
    el usuario en formato DD/MM/AAAA. No puede ser una fecha futura.
    Retorna la fecha (datetime) si es valida, o None si no lo es.
    """
    try:
        fecha = datetime.strptime(texto, "%d/%m/%Y")
    except ValueError:
        return None
    if fecha > datetime.now():
        return None
    return fecha


def validar_asunto(asunto):
    """
    Permite verificar que el asunto ingresado por el usuario sea
    correcto: de 5 a 150 caracteres, con letras, numeros, espacios
    y signos de puntuacion basicos.
    """
    if len(asunto) < 5 or len(asunto) > 150:
        return False
    permitidos = LETRAS + DIGITOS + SIGNOS_PUNTUACION + " "
    for caracter in asunto:
        if caracter not in permitidos:
            return False
    return True


def validar_descripcion(descripcion):
    """
    Permite verificar que la descripcion ingresada por el usuario
    sea correcta: debe contener de 20 a 2000 caracteres.
    """
    if len(descripcion) < 20 or len(descripcion) > 2000:
        return False
    return True


 
# RF-05: Flujo de estados
 
def siguiente_estado(estado_actual):
    """
    Permite identificar cual es el siguiente estado al que se puede
    pasar. Retorna None si la PQRS ya esta Solucionada.
    """
    posicion = ESTADOS.index(estado_actual)
    if posicion == len(ESTADOS) - 1:
        return None
    return ESTADOS[posicion + 1]
