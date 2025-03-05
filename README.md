# Análisis del Sector de Telecomunicaciones

## Descripción
Este proyecto realiza un análisis del sector de telecomunicaciones con énfasis en el acceso a internet. Utilizando técnicas de ETL y EDA, se busca identificar tendencias, posibles oportunidades de crecimiento y factores que afectan la calidad del servicio.

## Dataset
Los datos utilizados en este análisis provienen de [Fuente de Datos] e incluyen variables como:
- Cantidad de accesos a internet por región.
- Tipo de conexión (fibra óptica, ADSL, etc.).
- Evolución del mercado en los últimos años.

## Proceso de ETL & EDA
1. **ETL (Extracción, Transformación y Carga):**
   - Se limpiaron los datos eliminando valores nulos y duplicados.
   - Se normalizaron las columnas y se transformaron formatos.
   - Se integraron diversas fuentes de datos para mayor profundidad.

2. **EDA (Análisis Exploratorio de Datos):**
   - Se analizó la distribución de accesos a internet.
   - Se identificaron valores atípicos mediante boxplots.
   - Se estudió la evolución temporal del mercado.
   - Se comparó el acceso a internet según regiones y tecnologías.

## Dashboard con Streamlit
El dashboard interactivo permite visualizar:
- Tendencias en el acceso a internet.
- Comparaciones entre regiones y tipos de conexión.
- Identificación de valores atípicos en el sector.

### Ejecución del Dashboard
Para ejecutar el dashboard en local:
```bash
pip install streamlit pandas matplotlib plotly
streamlit run app.py
```

## Conclusiones Clave
- Existe una distribución desigual del acceso a internet.
- Se identificaron valores extremos que afectan la media.
- Ciertas tecnologías muestran un crecimiento acelerado en determinadas regiones.
