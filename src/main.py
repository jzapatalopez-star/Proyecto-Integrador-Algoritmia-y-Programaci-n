"""
Programa principal de SIPA, gestor de PQRS.

Muestra el menu y usa los modulos validaciones, archivos, radicado
y reportes.
"""

from datetime import datetime

import validaciones as v
import archivos
import radicado
import reportes

FORMATO_FECHA_HORA = "%d/%m/%Y %H:%M"
DIAS_RESPUESTA = 30


# Funciones de ayuda
def pedir_opcion(titulo, opciones):
    """
    Muestra una lista numerada y pide elegir una opcion.

    Repite la pregunta hasta que el usuario escriba un numero valido.
    Retorna el texto de la opcion elegida (no el numero).
    """
    print(titulo)
    for i in range(len(opciones)):
        print("   " + str(i + 1) + ". " + opciones[i])
    while True:
        eleccion = input("   Seleccione una opción: ")
        if v.es_numero(eleccion):
            numero = int(eleccion)
            if numero >= 1 and numero <= len(opciones):
                return opciones[numero - 1]
        print("  Opción inválida. Escriba un número de la lista.")


def mostrar_y_guardar_radicado(registro):
    """Muestra el radicado en pantalla y lo guarda como archivo .txt"""
    texto = radicado.generar_radicado(registro)
    print("\n" + texto)
    nombre_txt = "radicado_" + radicado.numero_radicado(registro) + ".txt"
    ruta = archivos.exportar_texto(nombre_txt, texto)
    print("Radicado guardado en: " + ruta)


# Opcion 1: Registrar PQRS
def registrar_pqrs():
    """Pide, valida y guarda una PQRS nueva e imprime el radicado."""
    print("\n--- REGISTRAR PQRS ---")
    print(">> Datos del solicitante")

    while True:
        nombre = input("Escriba su nombre completo: ")
        if v.validar_nombre(nombre):
            break
        print("  Dato inválido. Solo letras, espacios, ' o - (3 a 100).")

    # Lista con los nombres de los documentos (las claves del diccionario)
    nombres_documento = []
    for nombre_documento in v.TIPOS_DOCUMENTO:
        nombres_documento.append(nombre_documento)
    documento_elegido = pedir_opcion("Tipo de documento:", nombres_documento)
    sigla_documento = v.TIPOS_DOCUMENTO[documento_elegido]

    while True:
        numero_documento = input("Escriba su número de documento: ")
        if v.validar_numero_documento(numero_documento):
            break
        print("  Dato inválido. Solo números, entre 3 y 15 dígitos.")

    tipo_telefono = pedir_opcion("Tipo de teléfono:", v.TIPOS_TELEFONO)

    while True:
        telefono = input("Teléfono de contacto: ")
        if v.validar_telefono(telefono):
            break
        print("  Dato inválido. Debe tener exactamente 10 dígitos.")

    while True:
        correo = input("Correo electrónico: ")
        if v.validar_correo(correo):
            break
        print("  Dato inválido. Formato esperado: usuario@dominio.com")

    while True:
        direccion = input("Dirección (opcional, Enter para omitir): ")
        if v.validar_direccion(direccion):
            break
        print("  Dato inválido. De 5 a 200 caracteres; letras, números "
              "y # - . /")

    print("\n>> Información de la PQRS")
    tipo_solicitud = pedir_opcion("Tipo de solicitud:", v.TIPOS_SOLICITUD)

    while True:
        texto = input("Fecha de radicación (DD/MM/AAAA, Enter = hoy): ")
        if texto == "":
            fecha_radicacion = datetime.now()
            break
        fecha_radicacion = v.validar_fecha_radicacion(texto)
        if fecha_radicacion is not None:
            break
        print("  Dato inválido. Fecha incorrecta o futura.")

    canal = pedir_opcion("Canal de recepción:", v.CANALES)

    while True:
        asunto = input("Asunto o título: ")
        if v.validar_asunto(asunto):
            break
        print("  Dato inválido. De 5 a 150 caracteres; letras, números "
              "y puntuación.")

    while True:
        descripcion = input("Descripción detallada: ")
        if v.validar_descripcion(descripcion):
            break
        print("  Dato inválido. Mínimo 20 y máximo 2000 caracteres.")

    print("\n>> Información relacionada")
    mascota = pedir_opcion("Tipo de mascota:", v.MASCOTAS)
    campus = pedir_opcion("Campus relacionado:", v.CAMPUS)

    # RF-05: fecha maxima = fecha de registro + 30 dias
    fecha_registro = datetime.now()
    fecha_maxima = v.sumar_dias(fecha_registro, DIAS_RESPUESTA)

    registro = {
        "id": archivos.siguiente_id(tipo_solicitud),
        "nombre_completo": nombre,
        "tipo_documento": sigla_documento,
        "numero_documento": numero_documento,
        "tipo_telefono": tipo_telefono,
        "telefono_contacto": telefono,
        "correo_electronico": correo,
        "direccion": direccion,
        "tipo_solicitud": tipo_solicitud,
        "fecha_radicacion": fecha_radicacion.strftime("%d/%m/%Y"),
        "canal_recepcion": canal,
        "asunto_titulo": asunto,
        "descripcion_detallada": descripcion,
        "tipo_mascota": mascota,
        "campus_relacionado": campus,
        "fecha_registro": fecha_registro.strftime(FORMATO_FECHA_HORA),
        "fecha_maxima_respuesta": fecha_maxima.strftime(FORMATO_FECHA_HORA),
        "estado_peticion": "Registrada",
        "fecha_solucion": "",
    }
    archivos.guardar_registro(registro)
    mostrar_y_guardar_radicado(registro)
    print("\nPQRS registrada correctamente.")


# Opcion 2: Consultar PQRS
def elegir_pqrs():
    """
    Pide el tipo y el ID de una PQRS y la busca.

    Retorna la PQRS encontrada, o None si no existe.
    """
    tipo = pedir_opcion("Tipo de solicitud a buscar:", v.TIPOS_SOLICITUD)
    texto_id = input("ID del registro: ")
    if not v.es_numero(texto_id):
        print("  Dato inválido. El ID debe ser un número.")
        return None
    registro = archivos.buscar_registro(tipo, int(texto_id))
    if registro is None:
        print("  No existe una " + tipo + " con ese ID.")
    return registro


def listar_activas():
    """Muestra las PQRS que no estan solucionadas."""
    activas = []
    for registro in archivos.leer_todos():
        if registro["estado_peticion"] != "Solucionada":
            activas.append(registro)

    if len(activas) == 0:
        print("No hay PQRS activas.")
        return

    print("\nPQRS ACTIVAS: " + str(len(activas)))
    print(radicado.repetir("-", 70))
    for registro in activas:
        print(radicado.numero_radicado(registro)
              + " | " + registro["estado_peticion"]
              + " | Vence: " + registro["fecha_maxima_respuesta"])
        print("   Asunto: " + registro["asunto_titulo"])
    print(radicado.repetir("-", 70))


def consultar_pqrs():
    """Permite ver el listado de activas o el radicado de una PQRS."""
    print("\n--- CONSULTAR PQRS ---")
    opcion = pedir_opcion("¿Qué desea ver?",
                          ["Listado de PQRS activas",
                           "Radicado de una PQRS"])
    if opcion == "Listado de PQRS activas":
        listar_activas()
    else:
        registro = elegir_pqrs()
        if registro is not None:
            mostrar_y_guardar_radicado(registro)


# Opcion 3: Registrar cambio de estado
def cambiar_estado():
    """Avanza una PQRS al siguiente estado del flujo (RF-05)."""
    print("\n--- REGISTRAR CAMBIO EN PQRS ---")
    registro = elegir_pqrs()
    if registro is None:
        return

    actual = registro["estado_peticion"]
    nuevo = v.siguiente_estado(actual)
    if nuevo is None:
        print("Esta PQRS ya está Solucionada; no admite más cambios.")
        return

    print("Estado actual: " + actual + "  ->  nuevo estado: " + nuevo)
    confirmar = input("¿Confirmar cambio? (s/n): ")
    if confirmar != "s" and confirmar != "S":
        print("Cambio cancelado.")
        return

    registro["estado_peticion"] = nuevo
    if nuevo == "Solucionada":
        ahora = datetime.now()
        registro["fecha_solucion"] = ahora.strftime(FORMATO_FECHA_HORA)
    archivos.actualizar_registro(registro)
    print("Estado actualizado a " + nuevo)


# Opcion 4: Estadisticas
def ver_estadisticas():
    """Muestra las estadisticas y las exporta a un archivo plano."""
    texto = reportes.generar_reporte()
    print("\n" + texto)
    ruta = archivos.exportar_texto("reporte_estadisticas.txt", texto)
    print("\nReporte exportado en: " + ruta)


# Menu principal
def menu():
    """Muestra el menu principal hasta que el usuario elija Salir."""
    while True:
        print("\nBienvenido a SIPA - Gestión de PQRS")
        print("   1. Registrar PQRS")
        print("   2. Consultar PQRS")
        print("   3. Registrar Cambio en PQRS")
        print("   4. Estadísticas")
        print("   5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_pqrs()
        elif opcion == "2":
            consultar_pqrs()
        elif opcion == "3":
            cambiar_estado()
        elif opcion == "4":
            ver_estadisticas()
        elif opcion == "5":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción inválida.")


# Inicio del programa: crear los archivos si no existen y mostrar el menu
archivos.crear_archivos()
menu()
