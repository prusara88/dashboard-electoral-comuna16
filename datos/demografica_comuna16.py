"""
Datos demográficos de la Comuna 16 - Belén
Basado en:
- Anuario Estadístico de Medellín 2024
- Proyecciones DANE 2018-2030
- Alcaldía de Medellín
- Información pública y proyecciones estimadas

Población total Comuna 16: 217,501 habitantes (2024)
Densidad: 245.53 hab/ha
Extensión: 883.12 hectáreas
"""

import pandas as pd

# Datos demográficos por barrio
# Basados en proyecciones y distribución proporcional de la población total
DATOS_DEMOGRAFICOS = {
    'Belén': {
        'poblacion': 15800,
        'menores_15': 18,  # %
        'jovenes_15_29': 24,
        'adultos_30_59': 42,
        'mayores_60': 16,
        'estrato': 3.5,
        'parques': ['Parque Principal de Belén', 'Parque La Chinca'],
        'canchas': ['Cancha San Gabriel', 'Canchas Parque Belén'],
        'espacios': 'Parque Biblioteca de Belén, Parroquia Nuestra Señora de Belén',
        'coordinador': 'Rocío Bello',
        'contacto': '3008060115',
        'lideres_activos': 13
    },
    'Fátima': {
        'poblacion': 12500,
        'menores_15': 20,
        'jovenes_15_29': 26,
        'adultos_30_59': 40,
        'mayores_60': 14,
        'estrato': 3.2,
        'parques': ['Parque Fátima'],
        'canchas': ['Cancha de Fátima'],
        'espacios': 'Zona residencial consolidada',
        'coordinador': 'Laura Patricia Granada',
        'contacto': '3186008971',
        'lideres_activos': 8
    },
    'Rosales': {
        'poblacion': 11200,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.3,
        'parques': ['Parque Rosales'],
        'canchas': ['Cancha Rosales'],
        'espacios': 'Sector residencial',
        'coordinador': 'Rocío Bello',
        'contacto': '3008060115',
        'lideres_activos': 13
    },
    'Granada': {
        'poblacion': 9800,
        'menores_15': 17,
        'jovenes_15_29': 23,
        'adultos_30_59': 44,
        'mayores_60': 16,
        'estrato': 3.6,
        'parques': ['Parque Granada'],
        'canchas': [],
        'espacios': 'Zona residencial estrato medio',
        'coordinador': 'Mónica Bojaca',
        'contacto': '3218357548',
        'lideres_activos': 21
    },
    'San Bernardo': {
        'poblacion': 10500,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.4,
        'parques': ['Parque San Bernardo', 'Canchas de arena San Bernardo'],
        'canchas': ['Cancha de arena San Bernardo'],
        'espacios': 'Parque y zonas recreativas',
        'coordinador': 'Mónica Bojaca',
        'contacto': '3218357548',
        'lideres_activos': 21
    },
    'Las Playas': {
        'poblacion': 8900,
        'menores_15': 21,
        'jovenes_15_29': 27,
        'adultos_30_59': 39,
        'mayores_60': 13,
        'estrato': 2.9,
        'parques': ['Parque Las Playas'],
        'canchas': ['Cancha Las Playas'],
        'espacios': 'Sector popular',
        'coordinador': 'Clara Aida Villarraga',
        'contacto': '3135426444',
        'lideres_activos': 14
    },
    'Diego Echavarría': {
        'poblacion': 10800,
        'menores_15': 20,
        'jovenes_15_29': 26,
        'adultos_30_59': 40,
        'mayores_60': 14,
        'estrato': 3.1,
        'parques': ['Parque Diego Echavarría (renovado)'],
        'canchas': ['Canchas Diego Echavarría'],
        'espacios': 'Parque renovado en 2019',
        'coordinador': 'Clara Aida Villarraga',
        'contacto': '3135426444',
        'lideres_activos': 14
    },
    'La Mota': {
        'poblacion': 9200,
        'menores_15': 19,
        'jovenes_15_29': 24,
        'adultos_30_59': 42,
        'mayores_60': 15,
        'estrato': 3.3,
        'parques': ['Parque La Mota'],
        'canchas': [],
        'espacios': 'Zona residencial',
        'coordinador': 'Ramona Paz',
        'contacto': '3147796700',
        'lideres_activos': 26
    },
    'La Hondonada': {
        'poblacion': 8500,
        'menores_15': 18,
        'jovenes_15_29': 23,
        'adultos_30_59': 43,
        'mayores_60': 16,
        'estrato': 3.4,
        'parques': ['Parque La Hondonada'],
        'canchas': [],
        'espacios': 'Sector residencial',
        'coordinador': 'NA',
        'contacto': 'NA',
        'lideres_activos': 0
    },
    'El Rincón': {
        'poblacion': 9100,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.2,
        'parques': ['Parque El Rincón'],
        'canchas': ['Cancha El Rincón'],
        'espacios': 'Zona residencial con parque',
        'coordinador': 'Ramona Paz',
        'contacto': '3147796700',
        'lideres_activos': 26
    },
    'La Loma de Los Bernal': {
        'poblacion': 7800,
        'menores_15': 20,
        'jovenes_15_29': 26,
        'adultos_30_59': 40,
        'mayores_60': 14,
        'estrato': 2.8,
        'parques': ['Parque Loma de Los Bernal'],
        'canchas': [],
        'espacios': 'Sector popular',
        'coordinador': 'Juan Guillermo Ariola',
        'contacto': '3216154188',
        'lideres_activos': 22
    },
    'La Gloria': {
        'poblacion': 8600,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.1,
        'parques': ['Parque La Gloria'],
        'canchas': ['Cancha La Gloria'],
        'espacios': 'Zona residencial',
        'coordinador': 'Juan Guillermo Ariola',
        'contacto': '3216154188',
        'lideres_activos': 22
    },
    'Altavista': {
        'poblacion': 11500,
        'menores_15': 21,
        'jovenes_15_29': 27,
        'adultos_30_59': 39,
        'mayores_60': 13,
        'estrato': 2.7,
        'parques': ['Parque Altavista', 'Unidad Deportiva María Luisa Calle'],
        'canchas': ['Pista de patinaje María Luisa Calle', 'Canchas de squash', 'Canchas de fútbol'],
        'espacios': 'Unidad Deportiva completa (2007), pista skate, patinaje',
        'coordinador': 'Claudia Betancur',
        'contacto': '3005154172',
        'lideres_activos': 13
    },
    'La Palma': {
        'poblacion': 9400,
        'menores_15': 20,
        'jovenes_15_29': 26,
        'adultos_30_59': 40,
        'mayores_60': 14,
        'estrato': 3.0,
        'parques': ['Parque La Palma (renovado)'],
        'canchas': [],
        'espacios': 'Parque renovado programa 100 Parques',
        'coordinador': 'Paula Álvarez',
        'contacto': '3002404316',
        'lideres_activos': 14
    },
    'Los Alpes': {
        'poblacion': 10200,
        'menores_15': 18,
        'jovenes_15_29': 24,
        'adultos_30_59': 42,
        'mayores_60': 16,
        'estrato': 3.5,
        'parques': ['Parque de Los Alpes (renovado)'],
        'canchas': ['Canchas Los Alpes'],
        'espacios': 'Parque renovado, zonas deportivas',
        'coordinador': 'Paula Álvarez',
        'contacto': '3002404316',
        'lideres_activos': 14
    },
    'Las Violetas': {
        'poblacion': 9600,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.2,
        'parques': ['Parque Las Violetas'],
        'canchas': [],
        'espacios': 'Zona residencial',
        'coordinador': 'Isabel Jimenez',
        'contacto': '3004045093',
        'lideres_activos': 11
    },
    'Las Mercedes': {
        'poblacion': 10100,
        'menores_15': 18,
        'jovenes_15_29': 24,
        'adultos_30_59': 43,
        'mayores_60': 15,
        'estrato': 3.4,
        'parques': ['Parque Las Mercedes'],
        'canchas': ['Cancha Las Mercedes'],
        'espacios': 'Sector residencial consolidado',
        'coordinador': 'Isabel Jimenez',
        'contacto': '3004045093',
        'lideres_activos': 11
    },
    'Nueva Villa del Aburrá': {
        'poblacion': 9700,
        'menores_15': 20,
        'jovenes_15_29': 26,
        'adultos_30_59': 40,
        'mayores_60': 14,
        'estrato': 3.1,
        'parques': ['Parque Nueva Villa'],
        'canchas': [],
        'espacios': 'Zona residencial',
        'coordinador': 'Paula Álvarez',
        'contacto': '3002404316',
        'lideres_activos': 14
    },
    'Miravalle': {
        'poblacion': 10600,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.3,
        'parques': ['Parque Miravalle (renovado)'],
        'canchas': ['Canchas Miravalle'],
        'espacios': 'Parque renovado programa 100 Parques',
        'coordinador': 'Paula Álvarez',
        'contacto': '3002404316',
        'lideres_activos': 14
    },
    'El Nogal': {
        'poblacion': 8200,
        'menores_15': 18,
        'jovenes_15_29': 24,
        'adultos_30_59': 43,
        'mayores_60': 15,
        'estrato': 3.6,
        'parques': ['Parque El Nogal'],
        'canchas': [],
        'espacios': 'Zona residencial estrato medio-alto',
        'coordinador': 'Rocío Bello',
        'contacto': '3008060115',
        'lideres_activos': 13
    },
    'Los Almendros': {
        'poblacion': 7900,
        'menores_15': 17,
        'jovenes_15_29': 23,
        'adultos_30_59': 44,
        'mayores_60': 16,
        'estrato': 3.7,
        'parques': ['Parque Los Almendros'],
        'canchas': [],
        'espacios': 'Sector residencial consolidado',
        'coordinador': 'NA',
        'contacto': 'NA',
        'lideres_activos': 0
    },
    'Cerro Nutibara': {
        'poblacion': 14000,
        'menores_15': 19,
        'jovenes_15_29': 25,
        'adultos_30_59': 41,
        'mayores_60': 15,
        'estrato': 3.4,
        'parques': ['Cerro Nutibara (Morro Pelón - Ecoparque)', 'Pueblito Paisa'],
        'canchas': ['Unidad Deportiva Andrés Escobar Belén'],
        'espacios': 'Cerro Tutelar, ecoparque, senderos ecológicos, gimnasio al aire libre, pista atlética, pump track, parque infantil, parkour',
        'coordinador': 'Laura Patricia Granada',
        'contacto': '3186008971',
        'lideres_activos': 8
    }
}

def obtener_datos_demograficos():
    """
    Retorna DataFrame con datos demográficos
    """
    datos = []

    for barrio, info in DATOS_DEMOGRAFICOS.items():
        datos.append({
            'Barrio': barrio,
            'Población': info['poblacion'],
            'Menores_15_%': info['menores_15'],
            'Jóvenes_15_29_%': info['jovenes_15_29'],
            'Adultos_30_59_%': info['adultos_30_59'],
            'Mayores_60_%': info['mayores_60'],
            'Estrato_Promedio': info['estrato'],
            'Coordinador': info.get('coordinador', 'NA'),
            'Parques': ', '.join(info['parques']) if info['parques'] else 'Sin datos',
            'Canchas': ', '.join(info['canchas']) if info['canchas'] else 'Sin canchas registradas',
            'Espacios_Publicos': info['espacios']
        })

    return pd.DataFrame(datos)

def obtener_info_barrio(nombre_barrio):
    """
    Retorna información detallada de un barrio específico
    """
    return DATOS_DEMOGRAFICOS.get(nombre_barrio, None)

def obtener_datos_lideres():
    """
    Retorna DataFrame con cantidad de líderes activos por barrio
    Datos reales del archivo lideres.xlsx procesado
    Para usar en vista de Fuerza Electoral
    """
    from pathlib import Path

    # Intentar cargar datos reales del CSV procesado
    csv_path = Path(__file__).parent / 'lideres_por_barrio.csv'

    if csv_path.exists():
        # Cargar datos reales del CSV
        df_lideres = pd.read_csv(csv_path)
        df_lideres.columns = ['Barrio', 'Lideres_Activos']

        # Agregar información de coordinadores desde DATOS_DEMOGRAFICOS
        datos = []
        for _, row in df_lideres.iterrows():
            barrio = row['Barrio']
            info_barrio = DATOS_DEMOGRAFICOS.get(barrio, {})

            datos.append({
                'Barrio': barrio,
                'Lideres_Activos': int(row['Lideres_Activos']),
                'Coordinador': info_barrio.get('coordinador', 'NA'),
                'Contacto': info_barrio.get('contacto', 'NA')
            })

        return pd.DataFrame(datos)
    else:
        # Fallback a datos de DATOS_DEMOGRAFICOS si no existe el CSV
        datos = []
        for barrio, info in DATOS_DEMOGRAFICOS.items():
            datos.append({
                'Barrio': barrio,
                'Lideres_Activos': info.get('lideres_activos', 0),
                'Coordinador': info.get('coordinador', 'NA'),
                'Contacto': info.get('contacto', 'NA')
            })

        return pd.DataFrame(datos)
