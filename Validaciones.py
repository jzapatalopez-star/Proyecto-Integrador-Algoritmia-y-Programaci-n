{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP4qYY0bEspDjQldKKHzkrj",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/jzapatalopez-star/Proyecto-Integrador-Algoritmia-y-Programaci-n/blob/main/Validaciones.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "QeqT-DP9Jjab"
      },
      "outputs": [],
      "source": [
        "# caracteres para revisar los textos solicitados como: nombre, numero de documento\n",
        "LETRAS = (\"abcdefghijklmnopqrstuvwxyz\"\n",
        "          \"ABCDEFGHIJKLMNOPQRSTUVWXYZ\"\n",
        "          \"áéíóúÁÉÍÓÚñÑüÜ\")\n",
        "DIGITOS = \"0123456789\"\n",
        "SIGNOS_PUNTUACION = \".,;:¿?¡!()-\\\"'\"\n",
        "\n",
        "# Diccionario y listas para almacenar la información\n",
        "\n",
        "TIPOS_DOCUMENTO = {\n",
        "    \"Cédula de ciudadanía\": \"CC\",\n",
        "    \"Tarjeta de identidad\": \"TI\",\n",
        "    \"Cédula de extranjería\": \"CE\",\n",
        "    \"Pasaporte\": \"PP\",\n",
        "    \"NIT\": \"NIT\",\n",
        "}\n",
        "TIPOS_TELEFONO = [\"Celular\", \"Fijo\", \"Corporativo\", \"Otro\"]\n",
        "TIPOS_SOLICITUD = [\"Petición\", \"Queja\", \"Reclamo\", \"Sugerencia\"]\n",
        "CANALES = [\"Presencial\", \"Correo electrónico\", \"Página web\",\n",
        "           \"Teléfono\", \"Redes sociales\", \"Otro\"]\n",
        "MASCOTAS = [\"Perro\", \"Gato\"]\n",
        "CAMPUS = [\n",
        "    \"Campus Medellín - Ciudad Universitaria\",\n",
        "    \"Campus Medellín - Ciudadela Robledo\",\n",
        "    \"Campus en el Área de la salud\",\n",
        "    \"Campus Medellín - Sede de Posgrado\",\n",
        "    \"Campus Medellín - Edificio San Ignacio\",\n",
        "    \"Campus Medellín - Antigua Escuela de Derecho\",\n",
        "    \"Campus Medellín - Edificio Antioquia\",\n",
        "    \"Campus Medellín - Casas Patrimoniales\",\n",
        "    \"Campus Medellín - Edificio de Extensión\",\n",
        "\n",
        "# Estados para verificar la situación de la PQRS\n",
        "\n",
        "ESTADOS = [\"Registrada\", \"En proceso\", \"Solucionada\"]"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "##  RF-02: Validacion de los datos del solicitante"
      ],
      "metadata": {
        "id": "90pHhK7CJr7F"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_nombre(nombre):\n",
        "    \"\"\" Permite verificar que la información ingresada\n",
        "    por el usuario sea correcta, que contegna letras\n",
        "    y que el numero de los caracteres sea entre 3 a 100\n",
        "    \"\"\"\n",
        "    if len(nombre) < 3 or len(nombre) > 100:\n",
        "        return False\n",
        "    permitidos = LETRAS + \" '-\"\n",
        "    for letra in nombre:\n",
        "        if letra not in permitidos:\n",
        "            return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "KazdC0LNJuEs"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_numero_documento(numero_documento):\n",
        "    \"\"\" Permite verificar que la información ingresada\n",
        "    por el usuario sea correcta, que contegna solo digitos\n",
        "    y que el numero de los caracteres sea entre 3 a 15\n",
        "    \"\"\"\n",
        "    if len(numero_documento) < 3 or len(numero_documento) > 15:\n",
        "        return False\n",
        "    for digito in numero_documento:\n",
        "        if digito not in DIGITOS:\n",
        "            return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "4XvAmjK7J6CU"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_telefono(telefono):\n",
        "    \"\"\" Permite verificar que el numero telefónico\n",
        "    ingresado por el usuario solo contenga digitos,\n",
        "    y que sean exactamente 10\n",
        "    \"\"\"\n",
        "    if len(telefono) != 10:\n",
        "        return False\n",
        "    for digito in telefono:\n",
        "        if digito not in DIGITOS:\n",
        "            return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "lg8TyPLpKFLc"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_correo(correo):\n",
        "  \"\"\" Permite verificar que los datos ingresados por el usuario sean correctos,\n",
        "   debe tener menos de 254 caracteres,\n",
        "  además debe contener el signo arroba\n",
        "  y un punto antes de la última letra\n",
        "  \"\"\"\n",
        "    if len(correo) > 254 or \" \" in correo:\n",
        "        return False\n",
        "    if correo.count(\"@\") != 1:\n",
        "        return False\n",
        "    usuario, dominio = correo.split(\"@\")\n",
        "    if usuario == \"\" or \".\" not in dominio:\n",
        "        return False\n",
        "    if dominio[0] == \".\" or dominio[-1] == \".\":\n",
        "        return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "e-BeMQk0KNh_"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_direccion(direccion):\n",
        "  \"\"\" Permite verificar que el correo ingresada\n",
        "  por el usuario sea correcta,  si no lo ingresa es valido por ser un campo opcional,\n",
        "  si se escribe  puede contener caracteres alfanumericos y espacios y # - . /,\n",
        "  y  el numero de los caracteres deber ser entre 5 a 200\n",
        "  \"\"\"\n",
        "    if direccion == \"\":\n",
        "        return True\n",
        "    if len(direccion) < 5 or len(direccion) > 200:\n",
        "        return False\n",
        "    permitidos = LETRAS + DIGITOS + \" #-./,\"\n",
        "    for caracter in direccion:\n",
        "        if caracter not in permitidos:\n",
        "            return False\n",
        "    return True\n"
      ],
      "metadata": {
        "id": "tr6IVfcrKRp1"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "#  RF-03: Validacion de la informacion de la PQRS"
      ],
      "metadata": {
        "id": "-sMIO6bcKUjU"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_fecha_radicacion(texto):"
      ],
      "metadata": {
        "id": "5O6JXIUtKcDk"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_asunto(asunto):\n",
        "    \"\"\" Permite verificar que el asunto ingresado por el usuario sea correcto,\n",
        "    debe contener de 5 a 150 caracteres\n",
        "    \"\"\"\n",
        "    if len(asunto) < 5 or len(asunto) > 150:\n",
        "        return False\n",
        "    permitidos = LETRAS + DIGITOS + SIGNOS_PUNTUACION + \" \"\n",
        "    for caracter in asunto:\n",
        "        if caracter not in permitidos:\n",
        "            return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "JzlYci8CKfUM"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def validar_descripcion(descripcion):\n",
        "    \"\"\"\n",
        "    Permite verificar que la descripcion ingresada\n",
        "    por el usuario sea correcta:\n",
        "    debe contener de 20 a 2000 caracteres.\n",
        "    \"\"\"\n",
        "    if len(descripcion) < 20 or len(descripcion) > 2000:\n",
        "        return False\n",
        "    return True"
      ],
      "metadata": {
        "id": "3Cp0rE2eKnXE"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def siguiente_estado(estado_actual):\n",
        "    \"\"\" Permite identificar cual es el siguiente\n",
        "    estado al que se puede pasar\"\"\"\n",
        "\n",
        "\n",
        "    posicion = ESTADOS.index(estado_actual)\n",
        "    if posicion == len(ESTADOS) - 1:\n",
        "        return None\n",
        "    return ESTADOS[posicion + 1]"
      ],
      "metadata": {
        "id": "vc1b-l76KqZ0"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}