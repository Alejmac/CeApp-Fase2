import os
import json
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

def get_session(registro, password):
    url_login = 'https://ase1.ceti.mx/tecnologo/seguridad/iniciarsesion'
    datos_post = {'registro': registro, 'password': password}
    try:
        sesion = requests.Session()
        response = sesion.post(url_login, data=datos_post)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return None
    return sesion

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

def save_file(data, file_name):
    data_folder = os.path.join(os.getcwd(), 'Data')
    os.makedirs(data_folder, exist_ok=True)
    json_file_path = os.path.join(data_folder, file_name)

    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Extracción y guardado completados con éxito en {json_file_path}.")