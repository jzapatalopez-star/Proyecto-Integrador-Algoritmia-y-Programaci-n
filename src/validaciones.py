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


# Funcion de apoyo
def es_numero(texto):
    """
    Permite verificar que un texto tenga solo digitos y no este vacio.
    Se usa para revisar las opciones del menu y los ID.
    """
    if len(texto) == 0:
        return False
    for caracter in texto:
        if caracter not in DIGITOS:
            return False
    return True


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

    # Paso 1: contar los @ y guardar la posicion donde esta
    cantidad_arrobas = 0
    posicion_arroba = 0
    posicion = 0
    while posicion < len(correo):
        if correo[posicion] == "@":
            cantidad_arrobas = cantidad_arrobas + 1
            posicion_arroba = posicion
        posicion = posicion + 1
    if cantidad_arrobas != 1:
        return False

    # Paso 2: separar lo que va antes y despues del @
    usuario = correo[:posicion_arroba]
    dominio = correo[posicion_arroba + 1:]

    # Paso 3: revisar el usuario y el dominio
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

          
# Funciones de fechas
def dias_del_mes(mes, año):
    """Retorna cuantos dias tiene un mes en un año determinado."""
    dias_por_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if año % 4 == 0 and (año % 100 != 0 or año % 400 == 0):
        dias_por_mes[1] = 29        # año bisiesto: febrero tiene 29
    return dias_por_mes[mes - 1]


def sumar_dias(fecha, cantidad):
    """
    Retorna la fecha que resulta de sumarle una cantidad de dias.

    Avanza dia por dia; conserva la hora y los minutos.
    """
    dia = fecha.day
    mes = fecha.month
    año = fecha.year
    contador = 0
    while contador < cantidad:
        dia = dia + 1
        # Si se pasa del ultimo dia del mes, empieza el mes siguiente
        if dia > dias_del_mes(mes, año):
            dia = 1
            mes = mes + 1
            # Si el mes se pasa de diciembre, empieza el año siguiente
            if mes > 12:
                mes = 1
                año = año + 1
        contador = contador + 1
    nueva_fecha = datetime(año, mes, dia, fecha.hour, fecha.minute)
    return nueva_fecha

# RF-03: Validacion de la informacion de la PQRS


def validar_fecha_radicacion(texto):
    """
    Revisa la fecha de radicacion escrita como DD/MM/AAAA.

    Retorna la fecha (datetime) si es valida y no es futura,
    o None si no lo es.
    """
    # 1: la fecha debe tener 10 caracteres, por ejemplo 05/11/2026
    if len(texto) != 10:
        return None

    # 2: las barras deben estar en las posiciones 2 y 5
    if texto[2] != "/" or texto[5] != "/":
        return None

    # 3: los demas caracteres deben ser numeros
    posicion = 0
    while posicion < len(texto):
        if posicion != 2 and posicion != 5:
            if texto[posicion] not in DIGITOS:
                return None
        posicion = posicion + 1

    # 4: separar dia, mes y año y convertirlos a numeros
    dia = int(texto[0:2])
    mes = int(texto[3:5])
    año = int(texto[6:10])

    # 5: el mes debe estar entre 1 y 12
    if mes < 1 or mes > 12:
        return None

    # 6: el dia debe existir en ese mes
    if dia < 1 or dia > dias_del_mes(mes, año):
        return None

    # 7: el año debe ser razonable
    if año < 1900:
        return None

    # 8: crear la fecha y revisar que no sea futura
    fecha = datetime(año, mes, dia)
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
    sea correcta: de 20 a 2000 caracteres y que no sea solo espacios.
    """
    if len(descripcion) < 20 or len(descripcion) > 2000:
        return False
    # Debe tener al menos un caracter que no sea espacio
    for caracter in descripcion:
        if caracter != " ":
            return True
    return False


# RF-05: Flujo de estados
def siguiente_estado(estado_actual):
    """
    Permite identificar cual es el siguiente estado al que se puede
    pasar. Retorna None si la PQRS ya esta Solucionada.
    """
    if estado_actual == "Registrada":
        return "En proceso"
    elif estado_actual == "En proceso":
        return "Solucionada"
    else:
        return None
