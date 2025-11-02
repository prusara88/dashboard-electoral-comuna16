"""
Dashboard Electoral - Comuna 16 (Belén) - Medellín
Dashboard interactivo con 3 vistas de análisis
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json
import sys
import base64

# Agregar directorio de datos al path
sys.path.insert(0, str(Path(__file__).parent / "datos"))
from demografica_comuna16 import obtener_datos_demograficos, obtener_info_barrio, obtener_datos_lideres

# Cargar puestos de votación y casas de apoyo
PUESTOS_VOTACION_FILE = Path(__file__).parent / "datos" / "puestos_votacion_con_imagenes.csv"
CASAS_APOYO_FILE = Path(__file__).parent / "datos" / "casas_apoyo_geocodificadas.csv"

# Configuración de la página
st.set_page_config(
    page_title="Dashboard Electoral - Comuna 16",
    page_icon="🗳️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Rutas
DATA_DIR = Path("datos/geograficos")
GEOJSON_FILE = DATA_DIR / "barrios_comuna16_22barrios.geojson"

# Coordenadas del centro de Belén
BELEN_CENTER = [6.2204, -75.6068]
BELEN_ZOOM = 13

# Colores por vista
COLORES_VISTA = {
    "Demográfica": {
        "color_base": "#3498db",
        "escala": ["#ebf5fb", "#85c1e9", "#3498db", "#2874a6", "#1b4f72"]
    },
    "Fuerza Electoral": {
        "color_base": "#e74c3c",
        "escala": ["#fadbd8", "#f1948a", "#e74c3c", "#c0392b", "#922b21"]
    }
}

@st.cache_data
def cargar_datos_geograficos():
    """
    Carga el GeoJSON de los barrios
    """
    if not GEOJSON_FILE.exists():
        st.error(f"No se encuentra el archivo: {GEOJSON_FILE}")
        return None

    gdf = gpd.read_file(GEOJSON_FILE)
    return gdf

@st.cache_data
def cargar_puestos_votacion():
    """
    Carga los puestos de votación geocodificados
    """
    if not PUESTOS_VOTACION_FILE.exists():
        return None

    # Leer CSV con punto y coma como delimitador y coma como separador decimal
    df_puestos = pd.read_csv(PUESTOS_VOTACION_FILE, sep=';', decimal=',', encoding='latin-1')

    # Limpiar nombres de columnas (eliminar espacios en blanco)
    df_puestos.columns = df_puestos.columns.str.strip()

    # Verificar que existan las columnas necesarias
    columnas_requeridas = ['nombre', 'direccion', 'barrio', 'latitud', 'longitud', 'votacion']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df_puestos.columns]

    if columnas_faltantes:
        st.error(f"Faltan columnas en el archivo CSV: {columnas_faltantes}")
        st.error(f"Columnas encontradas: {list(df_puestos.columns)}")
        return None

    # Filtrar puestos con coordenadas válidas
    df_puestos = df_puestos.dropna(subset=['latitud', 'longitud'])

    # Asegurar que las coordenadas sean numéricas
    df_puestos['latitud'] = pd.to_numeric(df_puestos['latitud'], errors='coerce')
    df_puestos['longitud'] = pd.to_numeric(df_puestos['longitud'], errors='coerce')

    # Filtrar después de convertir
    df_puestos = df_puestos.dropna(subset=['latitud', 'longitud'])

    # Asegurar que la columna votacion sea numérica
    df_puestos['votacion'] = pd.to_numeric(df_puestos['votacion'], errors='coerce').fillna(0)

    return df_puestos

@st.cache_data
def cargar_casas_apoyo():
    """
    Carga las casas de apoyo geocodificadas
    """
    if not CASAS_APOYO_FILE.exists():
        return None

    # Leer CSV con punto y coma como delimitador y coma como separador decimal
    df_casas = pd.read_csv(CASAS_APOYO_FILE, sep=';', decimal=',', encoding='latin-1')

    # Limpiar nombres de columnas
    df_casas.columns = df_casas.columns.str.strip()

    # Verificar que existan las columnas necesarias
    columnas_requeridas = ['responsable', 'direccion', 'latitud', 'longitud']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df_casas.columns]

    if columnas_faltantes:
        st.warning(f"Faltan columnas en casas de apoyo: {columnas_faltantes}")
        return None

    # Asegurar que las coordenadas sean numéricas
    df_casas['latitud'] = pd.to_numeric(df_casas['latitud'], errors='coerce')
    df_casas['longitud'] = pd.to_numeric(df_casas['longitud'], errors='coerce')

    # Filtrar casas con coordenadas válidas
    df_casas = df_casas.dropna(subset=['latitud', 'longitud'])

    return df_casas

def crear_mapa_base(gdf, vista_seleccionada, datos_vista, df_puestos=None, df_casas=None):
    """
    Crea el mapa base con los barrios coloreados según la vista
    Para vista electoral, agrega marcadores de puestos de votación
    """
    # Crear mapa centrado en Belén
    mapa = folium.Map(
        location=BELEN_CENTER,
        zoom_start=BELEN_ZOOM,
        tiles='OpenStreetMap'
    )

    # Unir datos geográficos con datos de la vista
    gdf_con_datos = gdf.copy()

    # Determinar qué columna usar para colorear según la vista
    if vista_seleccionada == "Demográfica":
        # En vista demográfica, colorear por coordinador
        gdf_con_datos = gdf_con_datos.merge(datos_vista[['Barrio', 'Población', 'Coordinador']],
                                              left_on='NOMBRE', right_on='Barrio', how='left')

        # Paleta de colores por coordinador
        coordinadores_unicos = datos_vista['Coordinador'].unique()
        colores_coordinadores = {
            'Rocío Bello': '#3498db',          # Azul
            'Mónica Bojaca': '#e74c3c',        # Rojo
            'Juan Guillermo Ariola': '#2ecc71', # Verde
            'Ramona Paz': '#f39c12',           # Naranja
            'Laura Patricia Granada': '#9b59b6', # Morado
            'Paula Álvarez': '#1abc9c',        # Turquesa
            'Clara Aida Villarraga': '#e91e63', # Rosa
            'Isabel Jimenez': '#ff5722',       # Naranja oscuro
            'Claudia Betancur': '#795548',     # Marrón
            'NA': '#95a5a6'                     # Gris para sin coordinador
        }

        # Agregar polígonos coloreados por coordinador
        for idx, row in gdf_con_datos.iterrows():
            coordinador = row.get('Coordinador', 'NA')
            color = colores_coordinadores.get(coordinador, '#95a5a6')

            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color: {
                    'fillColor': color,
                    'color': '#333333',
                    'weight': 2,
                    'fillOpacity': 0.7
                }
            ).add_to(mapa)

    else:  # Fuerza Electoral
        columna_color = 'Lideres_Activos'
        gdf_con_datos = gdf_con_datos.merge(datos_vista[['Barrio', 'Lideres_Activos']],
                                              left_on='NOMBRE', right_on='Barrio', how='left')

        # Convertir a GeoJSON
        geojson_data = json.loads(gdf_con_datos.to_json())

        # Paleta de rojos para Fuerza Electoral: más oscuro = más líderes
        fill_color = 'Reds'
        legend_name = 'Líderes Activos'

        folium.Choropleth(
            geo_data=geojson_data,
            name='choropleth',
            data=gdf_con_datos,
            columns=['NOMBRE', columna_color],
            key_on='feature.properties.NOMBRE',
            fill_color=fill_color,
            fill_opacity=0.75,
            line_opacity=0.9,
            line_color='#333333',
            line_weight=2,
            legend_name=legend_name,
            nan_fill_color='lightgray',
            nan_fill_opacity=0.4
        ).add_to(mapa)

    # Agregar tooltips interactivos con información detallada
    if vista_seleccionada == "Demográfica":
        # Tooltips ricos para vista demográfica
        for idx, row in gdf_con_datos.iterrows():
            barrio_nombre = row['NOMBRE']
            info_barrio = obtener_info_barrio(barrio_nombre)

            if info_barrio:
                # Crear HTML personalizado para el tooltip
                tooltip_html = f"""
                <div style="font-family: Arial; font-size: 12px; width: 300px;">
                    <h4 style="margin: 0 0 10px 0; color: #2c3e50;">{barrio_nombre}</h4>

                    <p style="margin: 5px 0;"><b>Población:</b> {info_barrio['poblacion']:,} habitantes</p>

                    <p style="margin: 8px 0 3px 0;"><b>Distribución por edad:</b></p>
                    <ul style="margin: 0; padding-left: 20px;">
                        <li>Menores de 15: {info_barrio['menores_15']}%</li>
                        <li>Jóvenes 15-29: {info_barrio['jovenes_15_29']}%</li>
                        <li>Adultos 30-59: {info_barrio['adultos_30_59']}%</li>
                        <li>Mayores de 60: {info_barrio['mayores_60']}%</li>
                    </ul>

                    <p style="margin: 5px 0;"><b>Estrato:</b> {info_barrio['estrato']}</p>

                    <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">

                    <p style="margin: 5px 0;"><b>Coordinador Comité:</b> {info_barrio.get('coordinador', 'NA')}</p>
                    <p style="margin: 5px 0;"><b>Contacto:</b> {info_barrio.get('contacto', 'NA')}</p>
                    <p style="margin: 5px 0;"><b>Líderes Activos:</b> {info_barrio.get('lideres_activos', 0)}</p>

                    <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">

                    <p style="margin: 8px 0 3px 0;"><b>Parques:</b></p>
                    <p style="margin: 0 0 0 10px; font-size: 11px;">{', '.join(info_barrio['parques']) if info_barrio['parques'] else 'Sin datos'}</p>

                    <p style="margin: 8px 0 3px 0;"><b>Canchas deportivas:</b></p>
                    <p style="margin: 0 0 0 10px; font-size: 11px;">{', '.join(info_barrio['canchas']) if info_barrio['canchas'] else 'Sin canchas registradas'}</p>

                    <p style="margin: 8px 0 3px 0;"><b>Espacios públicos:</b></p>
                    <p style="margin: 0 0 0 10px; font-size: 11px;">{info_barrio['espacios']}</p>
                </div>
                """

                # Agregar el polígono con tooltip
                folium.GeoJson(
                    row['geometry'],
                    style_function=lambda x: {
                        'fillColor': 'transparent',
                        'color': 'transparent',
                        'weight': 0
                    },
                    tooltip=folium.Tooltip(tooltip_html, sticky=True)
                ).add_to(mapa)
    elif vista_seleccionada == "Fuerza Electoral":
        # Tooltips ricos para vista electoral con info de líderes
        for idx, row in gdf_con_datos.iterrows():
            barrio_nombre = row['NOMBRE']

            # Obtener cantidad de líderes del dato mapeado (datos reales)
            lideres = row.get('Lideres_Activos', 0)
            if pd.isna(lideres):
                lideres = 0

            # Obtener info adicional del barrio
            info_barrio = obtener_info_barrio(barrio_nombre)

            if info_barrio:
                coordinador = info_barrio.get('coordinador', 'Sin asignar')
                contacto = info_barrio.get('contacto', 'NA')
            else:
                coordinador = 'Sin asignar'
                contacto = 'NA'

            # Determinar color del título según cantidad de líderes
            if lideres >= 20:
                color_titulo = '#8B0000'  # Rojo oscuro
            elif lideres >= 10:
                color_titulo = '#c0392b'  # Rojo medio
            else:
                color_titulo = '#e74c3c'  # Rojo claro

            # Crear HTML personalizado para el tooltip electoral
            tooltip_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 280px;">
                <h4 style="margin: 0 0 10px 0; color: {color_titulo};">{barrio_nombre}</h4>

                <p style="margin: 5px 0; font-size: 14px;"><b>Líderes Activos:</b> <span style="font-size: 20px; color: {color_titulo}; font-weight: bold;">{int(lideres)}</span></p>

                <hr style="margin: 8px 0; border: none; border-top: 1px solid #ddd;">

                <p style="margin: 5px 0;"><b>Coordinador de Comité:</b></p>
                <p style="margin: 0 0 5px 10px; font-size: 11px;">{coordinador}</p>

                <p style="margin: 5px 0;"><b>Contacto:</b> {contacto}</p>
            </div>
            """

            # Agregar el polígono con tooltip
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x: {
                    'fillColor': 'transparent',
                    'color': 'transparent',
                    'weight': 0
                },
                tooltip=folium.Tooltip(tooltip_html, sticky=True)
            ).add_to(mapa)

    # PRIMERO: Agregar marcadores de casas de apoyo (para que queden abajo)
    if vista_seleccionada == "Fuerza Electoral" and df_casas is not None:
        for idx, row in df_casas.iterrows():
            # Crear HTML para popup de casa de apoyo
            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 250px;">
                <h4 style="margin: 0 0 10px 0; color: #2874A6; font-size: 14px;">Casa de Apoyo</h4>
                <p style="margin: 5px 0;"><b>Responsable:</b></p>
                <p style="margin: 0 0 5px 10px; font-size: 13px;">{row['responsable']}</p>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #ddd;">
                <p style="margin: 5px 0; font-size: 11px;"><b>Dirección:</b><br>{row['direccion']}</p>
            </div>
            """

            # Agregar marcador con ícono azul
            folium.Marker(
                location=[row['latitud'], row['longitud']],
                icon=folium.Icon(
                    color='blue',
                    icon='home',
                    prefix='fa'
                ),
                tooltip=folium.Tooltip(
                    f"<b>Casa de Apoyo</b><br>{row['responsable']}",
                    sticky=True
                ),
                popup=folium.Popup(popup_html, max_width=280)
            ).add_to(mapa)

    # SEGUNDO: Agregar puestos de votación (para que queden encima y no se tapen)
    if vista_seleccionada == "Fuerza Electoral" and df_puestos is not None:
        # Calcular min y max de votación para normalizar colores
        votacion_min = df_puestos['votacion'].min()
        votacion_max = df_puestos['votacion'].max()

        for idx, row in df_puestos.iterrows():
            # Preparar información del coordinador
            # Verificar si tiene coordinador (manejar NaN y 'NA')
            tiene_coordinador = False
            if pd.notna(row.get('coordinador_nombre')):
                if str(row['coordinador_nombre']).upper() != 'NA':
                    tiene_coordinador = True

            if tiene_coordinador:
                coordinador = f"{row['coordinador_nombre']} {row['coordinador_apellido']}"
                coordinador_html = f"<p style='margin: 5px 0;'><b>Coordinador(a):</b> {coordinador}</p>"
            else:
                coordinador_html = "<p style='margin: 5px 0; color: #888;'><i>Sin coordinador asignado</i></p>"

            # Obtener votación y calcular intensidad de color
            votacion = row['votacion']

            # Normalizar votación entre 0 y 1
            if votacion_max > votacion_min:
                intensidad = (votacion - votacion_min) / (votacion_max - votacion_min)
            else:
                intensidad = 0.5

            # Crear escala de rojos: más oscuro = más votación
            # RGB para rojo oscuro: (139, 0, 0) = #8B0000
            # RGB para rojo claro: (255, 182, 193) = #FFB6C1
            r = int(139 + (255 - 139) * (1 - intensidad))
            g = int(0 + (182 - 0) * (1 - intensidad))
            b = int(0 + (193 - 0) * (1 - intensidad))
            color_fill = f'#{r:02x}{g:02x}{b:02x}'

            # Color del borde siempre más oscuro
            color_border = '#8B0000'

            # Crear popup con información completa incluyendo votación e imagen
            # Verificar si tiene imagen local disponible
            imagen_html = ""
            if pd.notna(row.get('imagen_local')) and row['imagen_local']:
                # Convertir ruta relativa a ruta absoluta
                imagen_path = Path(__file__).parent / row['imagen_local']
                if imagen_path.exists():
                    # Leer y codificar la imagen en base64
                    with open(imagen_path, 'rb') as img_file:
                        img_data = base64.b64encode(img_file.read()).decode()

                    imagen_html = f"""
                    <div style="margin: 10px 0;">
                        <img src="data:image/jpeg;base64,{img_data}" style="width: 100%; max-width: 400px; border-radius: 5px; border: 2px solid #c0392b;" alt="Foto del puesto">
                    </div>
                    """

            popup_html = f"""
            <div style="font-family: Arial; font-size: 12px; width: 400px;">
                <h4 style="margin: 0 0 10px 0; color: #c0392b; font-size: 14px;">{row['nombre']}</h4>
                {imagen_html}
                <p style="margin: 5px 0;"><b>Barrio:</b> {row['barrio']}</p>
                <p style="margin: 5px 0; font-size: 11px;"><b>Dirección:</b><br>{row['direccion']}</p>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #ddd;">
                <p style="margin: 5px 0;"><b>Votación:</b> <span style="font-size: 16px; color: #c0392b; font-weight: bold;">{int(votacion)}</span></p>
                {coordinador_html}
            </div>
            """

            # Agregar círculo con color según votación (con zIndexOffset para que quede encima)
            folium.CircleMarker(
                location=[row['latitud'], row['longitud']],
                radius=8,
                color=color_border,
                fill=True,
                fillColor=color_fill,
                fillOpacity=0.8,
                weight=2,
                tooltip=folium.Tooltip(
                    f"<b>{row['nombre']}</b><br>Votación: {int(votacion)}",
                    sticky=True
                ),
                popup=folium.Popup(popup_html, max_width=450)
            ).add_to(mapa)

    return mapa

def mostrar_estadisticas_vista(datos_vista, vista_seleccionada):
    """
    Muestra estadísticas según la vista seleccionada
    """
    if vista_seleccionada == "Demográfica":
        # Indicadores principales demográficos
        col1, col2, col3, col4 = st.columns(4)

        poblacion_total = datos_vista['Población'].sum()

        # Calcular promedios ponderados de grupos de edad
        peso_menores = (datos_vista['Población'] * datos_vista['Menores_15_%']).sum() / poblacion_total
        peso_jovenes = (datos_vista['Población'] * datos_vista['Jóvenes_15_29_%']).sum() / poblacion_total
        peso_adultos = (datos_vista['Población'] * datos_vista['Adultos_30_59_%']).sum() / poblacion_total
        peso_mayores = (datos_vista['Población'] * datos_vista['Mayores_60_%']).sum() / poblacion_total

        estrato_promedio = datos_vista['Estrato_Promedio'].mean()

        with col1:
            st.metric("Población Total", f"{poblacion_total:,}")

        with col2:
            st.metric("Estrato Promedio", f"{estrato_promedio:.1f}")

        with col3:
            # Grupo etario predominante
            grupos = {
                'Menores 15': peso_menores,
                'Jóvenes 15-29': peso_jovenes,
                'Adultos 30-59': peso_adultos,
                'Mayores 60': peso_mayores
            }
            grupo_mayor = max(grupos, key=grupos.get)
            st.metric("Grupo Predominante", grupo_mayor.split()[0], f"{grupos[grupo_mayor]:.1f}%")

        with col4:
            # Población joven (menores de 30)
            poblacion_joven = peso_menores + peso_jovenes
            st.metric("Población < 30 años", f"{poblacion_joven:.1f}%")

    elif vista_seleccionada == "Fuerza Electoral":
        col1, col2, col3, col4 = st.columns(4)

        total_lideres = datos_vista['Lideres_Activos'].sum()
        promedio_lideres = datos_vista['Lideres_Activos'].mean()
        barrio_max = datos_vista.loc[datos_vista['Lideres_Activos'].idxmax()]
        barrios_con_lideres = (datos_vista['Lideres_Activos'] > 0).sum()

        with col1:
            st.metric("Total Líderes Activos", f"{total_lideres}")
        with col2:
            st.metric("Promedio por Barrio", f"{promedio_lideres:.1f}")
        with col3:
            st.metric("Barrio con Más Líderes", f"{barrio_max['Barrio']}", f"{int(barrio_max['Lideres_Activos'])} líderes")
        with col4:
            st.metric("Barrios con Líderes", f"{barrios_con_lideres}/22")

def crear_graficos_vista(datos_vista, vista_seleccionada):
    """
    Crea gráficos complementarios según la vista
    """
    if vista_seleccionada == "Demográfica":
        # Gráfico de barras - Población por barrio
        fig = px.bar(
            datos_vista.sort_values('Población', ascending=True).tail(10),
            x='Población',
            y='Barrio',
            orientation='h',
            title='Top 10 Barrios por Población',
            color='Población',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig, use_container_width=True)

    elif vista_seleccionada == "Fuerza Electoral":
        # Gráfico de barras - Líderes activos por barrio
        fig = px.bar(
            datos_vista.sort_values('Lideres_Activos', ascending=True).tail(15),
            x='Lideres_Activos',
            y='Barrio',
            orientation='h',
            title='Top 15 Barrios por Líderes Activos',
            color='Lideres_Activos',
            color_continuous_scale='Reds',
            labels={'Lideres_Activos': 'Líderes Activos'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

def main():
    """
    Función principal del dashboard
    """
    # Título
    st.title("🗳️ Dashboard Electoral - Comuna 16 (Belén)")
    st.markdown("### Medellín, Antioquia, Colombia")

    # Cargar datos geográficos, puestos de votación y casas de apoyo
    gdf = cargar_datos_geograficos()
    if gdf is None:
        st.error("No se pudieron cargar los datos geográficos")
        return

    df_puestos = cargar_puestos_votacion()
    df_casas = cargar_casas_apoyo()

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuración")

        # Selector de vista
        st.subheader("📊 Seleccionar Vista")
        vista_seleccionada = st.radio(
            "Tipo de análisis:",
            ["Demográfica", "Fuerza Electoral"],
            index=1
        )

        st.markdown("---")

        # Información de la vista
        if vista_seleccionada == "Demográfica":
            st.info("""
            **Vista Demográfica**

            Análisis de población y características sociodemográficas por barrio.
            """)
        elif vista_seleccionada == "Fuerza Electoral":
            st.info("""
            **Vista Fuerza Electoral**

            Análisis de resultados electorales, participación y potencial de crecimiento.
            """)

        st.markdown("---")
        if vista_seleccionada == "Demográfica":
            st.caption("✅ Vista demográfica con datos reales")

            # Leyenda de coordinadores
            st.markdown("### Coordinadores de Comité")

            coordinadores_colores = [
                ("Rocío Bello", "#3498db"),
                ("Mónica Bojaca", "#e74c3c"),
                ("Juan Guillermo Ariola", "#2ecc71"),
                ("Ramona Paz", "#f39c12"),
                ("Laura Patricia Granada", "#9b59b6"),
                ("Paula Álvarez", "#1abc9c"),
                ("Clara Aida Villarraga", "#e91e63"),
                ("Isabel Jimenez", "#ff5722"),
                ("Claudia Betancur", "#795548"),
                ("Sin coordinador", "#95a5a6")
            ]

            for coordinador, color in coordinadores_colores:
                st.markdown(
                    f'<div style="display: flex; align-items: center; margin-bottom: 8px;">'
                    f'<div style="width: 20px; height: 20px; background-color: {color}; '
                    f'margin-right: 10px; border: 1px solid #333;"></div>'
                    f'<span style="font-size: 14px;">{coordinador}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        elif vista_seleccionada == "Fuerza Electoral":
            st.caption("✅ Líderes activos por barrio (datos reales)")
            if df_puestos is not None:
                st.caption(f"✅ {len(df_puestos)} puestos de votación mapeados")
            if df_casas is not None:
                st.caption(f"🏠 {len(df_casas)} casas de apoyo (azul)")

    # Cargar datos demográficos reales
    demografica_real = obtener_datos_demograficos()

    # Cargar datos de líderes para vista electoral
    datos_lideres = obtener_datos_lideres()

    # Seleccionar datos según vista
    if vista_seleccionada == "Demográfica":
        datos_vista = demografica_real
    else:  # Fuerza Electoral
        datos_vista = datos_lideres

    # Mostrar estadísticas principales
    st.subheader(f"📈 Indicadores - {vista_seleccionada}")
    mostrar_estadisticas_vista(datos_vista, vista_seleccionada)
    st.markdown("---")

    # Mapa solo - Ocupa todo el ancho
    st.subheader("🗺️ Mapa Interactivo")
    mapa = crear_mapa_base(gdf, vista_seleccionada, datos_vista, df_puestos, df_casas)
    st_folium(mapa, height=600, use_container_width=True)

    # Tabla y gráficos solo para vista electoral
    if vista_seleccionada == "Fuerza Electoral":
        st.markdown("---")

        # Tabla de datos debajo del mapa
        st.subheader("📋 Datos por Barrio")
        st.dataframe(
            datos_vista.sort_values('Barrio'),
            use_container_width=True
        )

        st.markdown("---")

        # Gráficos complementarios
        st.subheader(f"📊 Análisis Detallado - {vista_seleccionada}")
        crear_graficos_vista(datos_vista, vista_seleccionada)

    # Footer
    st.markdown("---")
    st.caption("Dashboard Electoral Comuna 16 - Belén | Desarrollado con Streamlit")

if __name__ == "__main__":
    main()
