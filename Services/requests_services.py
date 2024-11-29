import json
import requests
from bs4 import BeautifulSoup
import os
#from kivy.utils import platform
#from plyer import storagepath
from unidecode import unidecode

def get_session(registro, password):
    url_login = 'https://ase1.ceti.mx/tecnologo/seguridad/iniciarsesion'
    datos_post = {'registro': registro, 'password': password}
    try:
        sesion = requests.Session()
        response_login = sesion.post(url_login, data=datos_post)
        response_login.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud de login: {e}")
        return None
    return sesion

def get_tira_materias(sesion):
    url_home = 'https://ase1.ceti.mx/tecnologo/tgoalumno/tiras'
    try:
        response_home = sesion.get(url_home)
        response_home.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

    soup = BeautifulSoup(response_home.content, 'html.parser')
    
    # Buscar la tabla específica de materias asignadas
    tabla_asignadas = soup.find('th', class_='naranja', text=lambda t: "LISTA DE MATERIAS ASIGNADAS PARA EL PERIODO" in t)
    
    if not tabla_asignadas:
        print("No se encontró la tabla de materias asignadas.")
        return None

    # Buscar las filas que contienen las materias asignadas
    materias = []
    filas = tabla_asignadas.find_parent('table').find_all('tr')[2:]  # Ignora el encabezado

    for fila in filas:
        columnas = fila.find_all('td')
        
        if len(columnas) >= 11:
            materia = {
                'clave': columnas[0].text.strip(),
                'nombre': columnas[1].text.strip(),
                'division': columnas[2].text.strip(),
                'profesor': columnas[3].text.strip(),
                'correo': columnas[4].text.strip(),
                'grupo': columnas[5].text.strip(),
                'tipo': columnas[6].text.strip(),
                'tipo_pond': columnas[7].text.strip(),
                'primer_parcial': columnas[8].text.strip() if columnas[8].text.strip() != '---' else None,
                'segundo_parcial': columnas[9].text.strip() if columnas[9].text.strip() != '---' else None,
                'tercer_parcial': columnas[10].text.strip() if columnas[10].text.strip() != '---' else None
            }
            materias.append(materia)

    return materias


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


def get_schedule(sesion):
    url_home = 'https://ase1.ceti.mx/tecnologo/tgoalumno/horario'

    try:
        response_home = sesion.get(url_home)
        response_home.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

    soup = BeautifulSoup(response_home.content, 'html.parser')

    def clean_text(text):
        return text.strip().replace('\xa0', '')

    def parse_horario_table(table):
        horario_json = {}
        rows = table.find_all('tr')
        
        # Obtener los días de la semana
        dias_semana = [clean_text(th.text) for th in rows[0].find_all('th')]
        
        # Iterar sobre las filas de la tabla, excluyendo la primera fila (encabezados de días)
        for row in rows[1:]:
            # Obtener las celdas de la fila actual
            cells = row.find_all(['th', 'td'])
    
            # La primera celda de cada fila contiene la hora
            hora = clean_text(cells[0].text)
    
            for dia, materia, materia_data in zip(dias_semana, cells[1:], cells[1:]):
                materia_text_list = materia.find_all('span', style='color:#1569C7; font-size:10px;')
                materia_data_text_list = materia_data.find_all('span', style='color:#FFFFFF;')
    
                # Procesar el texto de materia
                materia_text = [clean_text(span.text) for span in materia_text_list]
    
                # Procesar el texto de materia_data si es necesario
                materia_data_text = [clean_text(span.text) for span in materia_data_text_list]
    
                if dia not in horario_json:
                    horario_json[dia] = {}
    
                if materia_text:
                    horario_json[dia][hora] = {'materia': materia_text, 'materia_data': materia_data_text}
                else:
                    horario_json[dia][hora] = {'materia': '', 'materia_data': materia_data_text}
    
        return horario_json

    horario_tables = soup.find_all('table', {'class': 'tabla', 'style': 'font-size:10px;', 'width': '100%'})

    horario_final = {}
    for table in horario_tables:
        horario_dia = parse_horario_table(table)
        horario_final.update(horario_dia)

    # Convertir el horario final a JSON
    # horario_json = json.dumps(horario_final, ensure_ascii=False, indent=2)

    return horario_final

def get_student(sesion):
    url_home = 'https://ase1.ceti.mx/tecnologo/tgoalumno/tiras'

    try:
        response_home = sesion.get(url_home)
        response_home.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None

    soup = BeautifulSoup(response_home.content, 'html.parser')

    materias_table = soup.find('table', {'class': 'tabla'})
    if materias_table is None:
        raise ValueError("No se encontró ninguna tabla con los atributos especificados en el documento HTML.")

    def no_contiene_correo(tag):
        return tag.name == 'td' and not tag.text.strip().startswith("Guía para activar el correo:")

    etiquetas_td_k = soup.find_all(no_contiene_correo, {'class': ['naranja', 'azul']})

    etiquetas_td = soup.find_all(['td', 'th'], {'class': ['gris', 'rojo'], 'colspan': False})

    def clean_key(key):
        key_without_accents = unidecode(key)
        key_cleaned = key_without_accents.replace(':', '')
        key_cleaned = key_cleaned.replace('del', '')
        key_cleaned = key_cleaned.replace('de', '')
        key_cleaned = key_cleaned.replace(' ', '')
        return key_cleaned

    data_cleaned = {}
    count = 0

    for k, v in zip(etiquetas_td_k, etiquetas_td):
        key_cleaned = clean_key(k.text.strip())
        data_cleaned[key_cleaned] = v.text.strip()
        count += 1
        if count == 25:
            break

    data_folder = os.path.join(os.getcwd(), 'Data')

    os.makedirs(data_folder, exist_ok=True)
    json_file_path = os.path.join(data_folder, 'data_cleaned.json')

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data_cleaned, file, ensure_ascii=False, indent=2)

    print(f"Extracción y guardado completados con éxito en {json_file_path}.")
    return data_cleaned

def parse_kardex(session):
    url = 'https://ase1.ceti.mx/tecnologo/tgoalumno/kardex'
    response = session.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar específicamente la tabla deseada
    table = soup.find('table', {'class': 'tabla', 'width': '90%'})

    if not table:
        raise ValueError("La tabla especificada no se encontró en el HTML.")

    kardex_data = {}
    current_level = None  # Nivel actual
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all(['td', 'th'])
        headers = row.find_all('th')

        # Detectar si es una fila de nivel
        if headers and 'Nivel' in headers[0].text:
            current_level = headers[0].text.strip()  # Extraer nombre del nivel
            kardex_data[current_level] = {'materias': [], 'promedio': 0}
        elif cols and current_level is not None:
            # Verificar que la fila tenga columnas válidas
            if len(cols) >= 5:
                clave = cols[0].text.strip()
                nombre = cols[1].text.strip()
                tipo = cols[2].text.strip()
                periodo = cols[4].text.strip()
                promedio_text = cols[3].text.strip()
                promedio = int(promedio_text) if promedio_text.isdigit() else 0  # Validar promedio

                # Agregar la materia al nivel actual
                kardex_data[current_level]['materias'].append({
                    'clave': clave,
                    'nombre': nombre,
                    'tipo': tipo,
                    'periodo': periodo,
                    'promedio': promedio
                })

    # Calcular promedios por nivel y general
    total_promedios = 0
    total_materias = 0

    for level, data in kardex_data.items():
        materias = data['materias']
        if materias:
            # Filtrar solo materias evaluadas (promedio > 0)
            materias_evaluadas = [m for m in materias if m['promedio'] > 0]
            total_nivel = sum(m['promedio'] for m in materias_evaluadas)
            count_nivel = len(materias_evaluadas)
            promedio_nivel = round(total_nivel / count_nivel, 2) if count_nivel > 0 else 0
            kardex_data[level]['promedio'] = promedio_nivel

            # Sumar al promedio general
            total_promedios += total_nivel
            total_materias += count_nivel

    promedio_general = round(total_promedios / total_materias, 2) if total_materias > 0 else 0
    kardex_data['promedio_general'] = promedio_general
    return kardex_data

def save_file(data, file_name):
    
    data_folder = os.path.join(os.getcwd(), 'Data')
    os.makedirs(data_folder, exist_ok=True)
    json_file_path = os.path.join(data_folder, file_name)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Extracción y guardado completados con éxito en {json_file_path}.")