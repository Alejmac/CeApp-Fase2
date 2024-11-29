import os
import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_session(registro, password):
    """
    Realiza el inicio de sesión en la plataforma y devuelve la sesión activa.
    """
    url_login = 'https://ase1.ceti.mx/tecnologo/seguridad/iniciarsesion'
    datos_post = {'registro': registro, 'password': password}
    try:
        sesion = requests.Session()
        response = sesion.post(url_login, data=datos_post)
        response.raise_for_status()
        return sesion
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None


def clean_text(text):
    """
    Limpia texto eliminando caracteres no deseados como saltos de línea y espacios en blanco.
    """
    return text.replace('\xa0', '').replace('\n', '').strip()


def extraer_keys():
    """
    Devuelve las claves necesarias para estructurar los datos de la tabla.
    """
    return [
        "CLAVE",
        "NIVEL",
        "MATERIA",
        "PROFESOR",
        "ESTATUS MATERIA",
        "TIPO POND.",
        "1ER. PARCIAL (Faltas)",
        "1ER. PARCIAL (Calf. Captura)",
        "1ER. PARCIAL (Calf. Pond.)",
        "2DO. PARCIAL (Faltas)",
        "2DO. PARCIAL (Calf. Captura)",
        "2DO. PARCIAL (Calf. Pond.)",
        "3RO. PARCIAL (Faltas)",
        "3RO. PARCIAL (Calf. Captura)",
        "3RO. PARCIAL (Calf. Pond.)",
        "FINAL (Faltas)",
        "FINAL (Calf.)"
    ]


def calcular_ponderacion(tipo_pond):
    """
    Devuelve las ponderaciones según el tipo.
    Si el tipo es '-' o nulo, asigna el tipo 'C' (33%, 33%, 34%).
    """
    ponderaciones = {
        "A": [0.2, 0.35, 0.45],
        "B": [0.15, 0.35, 0.5],
        "C": [0.33, 0.33, 0.34],
    }
    return ponderaciones.get(tipo_pond, ponderaciones["C"])


def calcular_calificaciones(grade_dict):
    """
    Calcula la sumatoria de calificaciones ponderadas y cuánto falta para 70.
    """
    tipo_pond = grade_dict.get("TIPO POND.")
    ponderacion = calcular_ponderacion(tipo_pond)

    # Obtener calificaciones parciales
    parciales = [
        grade_dict.get("1ER. PARCIAL (Calf. Captura)", "-"),
        grade_dict.get("2DO. PARCIAL (Calf. Captura)", "-"),
        grade_dict.get("3RO. PARCIAL (Calf. Captura)", "-"),
    ]

    # Convertir las calificaciones a flotantes, usar 0 para los vacíos o no válidos
    calificaciones = [float(c) if c.replace('.', '', 1).isdigit() else 0 for c in parciales]

    # Calcular el total ponderado
    total_ponderado = sum(c * p for c, p in zip(calificaciones, ponderacion))

    # Determinar cuánto falta para llegar a 70
    falta = max(0, (70 - total_ponderado) / ponderacion[-1])

    return {
        "Total Ponderado": round(total_ponderado, 2),
        "Falta para 70": round(falta, 2),
    }


def parsear_tabla(table):
    """
    Parsea la tabla de calificaciones y devuelve los datos en formato JSON.
    """
    keys = extraer_keys()
    grades_json = {}
    rows = table.find_all('tr')[2:]  # Saltar encabezados

    for row in rows:
        cells = row.find_all('td')
        if cells:
            values = [clean_text(cell.text) for cell in cells]
            # Ajustar el número de valores para que coincida con las claves
            values.extend(["-"] * (len(keys) - len(values)))
            values = values[:len(keys)]

            # Crear un diccionario con las claves y valores
            clave = values[0] if values[0] != "-" else f"Unnamed_{len(grades_json) + 1}"
            grade_dict = dict(zip(keys, values))

            # Calcular datos adicionales
            grade_dict.update(calcular_calificaciones(grade_dict))
            if clave:
                grades_json[clave] = grade_dict

    return grades_json


def get_grades(sesion):
    """
    Obtiene las calificaciones del usuario desde la página y las procesa.
    """
    url_home = 'https://ase1.ceti.mx/tecnologo/tgoalumno/calificaciones'
    try:
        response = sesion.get(url_home)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Buscar el div y la tabla de calificaciones
        div_cal = soup.find('div', {'id': 'cal'})
        if not div_cal:
            raise ValueError("No se encontró el div con id 'cal'.")
        table = div_cal.find('table', {'class': 'tabla'})
        if not table:
            raise ValueError("No se encontró la tabla de calificaciones.")

        # Procesar la tabla
        return parsear_tabla(table)
    except Exception as e:
        print(f"Error al obtener calificaciones: {e}")
        return None


def save_file(data, file_name="calificaciones.json"):
    """
    Guarda los datos en un archivo JSON dentro de la carpeta 'Data'.
    """
    folder = os.path.join(os.getcwd(), 'Data')
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, file_name)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        print(f"Datos guardados correctamente en {file_path}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


# Ejecución principal
if __name__ == "__main__":
    registro = '21110191'
    password = '123asdzX'
    sesion = get_session(registro, password)

    if sesion:
        calificaciones = get_grades(sesion)
        if calificaciones:
            pprint(calificaciones)
            # save_file(calificaciones)
