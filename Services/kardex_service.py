import requests
from bs4 import BeautifulSoup
import re

 
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
            total_nivel = sum(m['promedio'] for m in materias)
            count_nivel = len(materias)
            promedio_nivel = total_nivel / count_nivel if count_nivel > 0 else 0
            kardex_data[level]['promedio'] = promedio_nivel

            # Sumar al promedio general
            total_promedios += total_nivel
            total_materias += count_nivel

    promedio_general = total_promedios / total_materias if total_materias > 0 else 0
    kardex_data['promedio_general'] = promedio_general

    return kardex_data

