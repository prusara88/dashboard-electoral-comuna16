# 🗳️ Dashboard Electoral - Comuna 16 (Belén)

Dashboard interactivo para análisis electoral de la Comuna 16 - Belén, Medellín, Colombia.

## 📊 Características

- **Vista Demográfica**: Análisis poblacional y características sociodemográficas por barrio
- **Vista Fuerza Electoral**: Análisis de líderes activos, puestos de votación y casas de apoyo
- **Mapa Interactivo**: Visualización de 22 barrios con información detallada
- **25 Puestos de Votación**: Con fotos y datos de votación
- **10 Casas de Apoyo**: Ubicación y responsables
- **Datos de Líderes**: 188 líderes activos distribuidos por barrio
- **Coordinadores de Comité**: Organización territorial por coordinador

## 🚀 Demo en Vivo

[Ver Dashboard](https://share.streamlit.io/) _(Agregar tu URL cuando esté desplegado)_

## 🛠️ Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/dashboard-electoral-comuna16.git
cd dashboard-electoral-comuna16

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

El dashboard se abrirá automáticamente en: http://localhost:8501

## 📁 Estructura del Proyecto

```
dashboard-electoral-comuna16/
├── app.py                                    # Aplicación principal
├── requirements.txt                          # Dependencias Python
│
└── datos/
    ├── demografica_comuna16.py              # Datos demográficos de 22 barrios
    ├── lideres_por_barrio.csv               # Líderes activos por barrio
    ├── casas_apoyo_geocodificadas.csv       # 10 casas de apoyo geocodificadas
    ├── puestos_votacion_con_imagenes.csv    # 25 puestos con fotos
    │
    ├── imagenes_puestos/                    # Fotos de puestos de votación
    │   └── *.jpg                            # 23 imágenes de Google Street View
    │
    └── geograficos/
        └── barrios_comuna16_22barrios.geojson  # Polígonos de barrios
```

## 📈 Datos Incluidos

### Barrios (22 total)
Altavista, Belén, Diego Echavarría, El Rincón, Fátima, Granizal, Granada, La Gloria, La Hondonada, La Mota, La Palma, Las Violetas, Los Alpes, Miravalle, Nueva Villa del Aburra, El Nogal, Rosales, San Bernardo, Cerro Nutibara, Los Almendros, Las Mercedes, La Loma de los Bernal

### Datos Demográficos
- Población por barrio
- Distribución por grupos de edad
- Estratos socioeconómicos
- Parques y espacios públicos

### Datos Electorales
- 188 líderes activos
- 25 puestos de votación geocodificados
- 10 casas de apoyo
- 9 coordinadores de comité

## 🗺️ Vistas del Dashboard

### Vista Demográfica
- Mapa coloreado por coordinador de comité
- Estadísticas poblacionales
- Distribución etaria
- Espacios públicos por barrio

### Vista Fuerza Electoral
- Mapa coloreado por cantidad de líderes (gradient)
- Puestos de votación con fotos (círculos rojos)
- Casas de apoyo (marcadores azules)
- Estadísticas de líderes por barrio

## 🛠️ Tecnologías Utilizadas

- **Streamlit**: Framework web
- **Folium**: Mapas interactivos
- **Pandas**: Procesamiento de datos
- **GeoPandas**: Datos geoespaciales
- **Plotly**: Gráficos interactivos

## 📝 Licencia

Este proyecto es de código abierto para uso electoral y comunitario.

## 👥 Contribuciones

Desarrollado para análisis electoral de la Comuna 16 - Belén, Medellín.
