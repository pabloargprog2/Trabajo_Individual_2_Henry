import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configurar la página al inicio
st.set_page_config(page_title="Accesos a Internet en Argentina", layout="wide")

# Cargar los datos 
@st.cache_data
def cargar_datos():
    df_totales = pd.read_excel('dataset_internet.xlsx', sheet_name='Totales Accesos Por Tecnología')
    df_penetracion = pd.read_excel('dataset_internet.xlsx', sheet_name='Penetracion-poblacion')
    df_accesos_tec = pd.read_excel('dataset_internet.xlsx', sheet_name='Accesos_tecnologia_localidad')
    df_ingresos = pd.read_excel('dataset_internet.xlsx', sheet_name='Ingresos')
    df_penetracion_hogares = pd.read_excel('internet.xlsx', sheet_name='Penetracion-hogares')
    return df_totales, df_penetracion, df_accesos_tec, df_ingresos, df_penetracion_hogares

df_totales, df_penetracion, df_accesos_tec,df_ingresos, df_penetracion_hogares = cargar_datos()

# Lista de tecnologías
tecnologias = ['ADSL', 'Cablemodem', 'Fibra óptica', 'Wireless', 'Otros']

# Convertir la columna de ingresos a numérica
df_ingresos['Ingresos (miles de pesos)'] = pd.to_numeric(df_ingresos['Ingresos (miles de pesos)'], errors='coerce')

# Agrupar por año
df_anual = df_ingresos.groupby('Año', as_index=False)['Ingresos (miles de pesos)'].sum()

# Página Totales accesos por tecnologia
def pagina_accesos_totales_tecnologia():
    st.header("📡 Accesos a Internet en Argentina por Tecnologia")

    # Filtros interactivos
    años_seleccionados = st.sidebar.multiselect(
        'Selecciona Años', 
        options=df_totales['Año'].unique(), 
        default=df_totales['Año'].unique()
    )

    tecnologias_seleccionadas = st.sidebar.multiselect(
        'Selecciona Tecnologías', 
        options=tecnologias, 
        default=tecnologias
    )

    # Filtrar los datos
    df_filtrado = df_totales[df_totales['Año'].isin(años_seleccionados)]

    # Gráfico de evolución de accesos
    df_evolucion = df_filtrado.groupby(['Año'])['Total'].sum().reset_index()

    st.subheader('Evolución de los Accesos Totales a Internet')
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df_evolucion['Año'], df_evolucion['Total'], marker='o', color='b')
    ax.set_title('Evolución de los Accesos Totales a Internet')
    ax.set_xlabel('Año')
    ax.set_ylabel('Accesos Totales')
    ax.grid(True)
    st.pyplot(fig)

    # Distribución de accesos por tecnología
    st.subheader('Distribución de Accesos por Tecnología')
    df_tecnologias = df_filtrado[tecnologias_seleccionadas].sum()

    fig, ax = plt.subplots(figsize=(10, 5))
    df_tecnologias.sort_values(ascending=False).plot(kind='bar', ax=ax, color='lightgreen', edgecolor='black')
    ax.set_title('Distribución de Accesos por Tecnología')
    ax.set_xlabel('Tecnología')
    ax.set_ylabel('Total de Accesos')
    st.pyplot(fig)

    # Matriz de correlación
    if len(tecnologias_seleccionadas) > 1:
        st.subheader('Matriz de Correlación entre Tecnologías de Acceso')
        corr = df_filtrado[tecnologias_seleccionadas].corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
        st.pyplot(fig)

    # Boxplot para análisis de valores extremos
    st.subheader('Boxplot de Tecnologías de Acceso a Internet')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df_filtrado[tecnologias_seleccionadas], ax=ax)
    ax.set_title('Boxplot de Tecnologías de Acceso a Internet')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

    # Mostrar tabla de datos filtrados
    st.subheader('Datos Filtrados')
    st.dataframe(df_filtrado)

# Página Análisis de Penetración de Internet
def pagina_penetracion():
    st.header("📈 Analisis de Penetracion de Internet")
    
    # Filtros
    anos = st.sidebar.multiselect("Selecciona uno o más años", df_penetracion["Año"].unique())
    provincias = st.sidebar.multiselect("Selecciona una o más provincias", df_penetracion["Provincia"].unique())
    
    # Filtrar datos según selección
    filtered_df_penetracion = df_penetracion.copy()
    
    if anos:
        filtered_df_penetracion = filtered_df_penetracion[filtered_df_penetracion["Año"].isin(anos)]
    if provincias:
        filtered_df_penetracion = filtered_df_penetracion[filtered_df_penetracion["Provincia"].isin(provincias)]

    st.write("### Distribución de Accesos por Cada 100 Habitantes")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(filtered_df_penetracion['Accesos por cada 100 hab'], kde=True, bins=30, color='skyblue', ax=ax)
    ax.set_xlabel("Accesos por cada 100 habitantes")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

    st.write("### Accesos por Cada 100 Habitantes por Provincia")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=filtered_df_penetracion, x='Provincia', y='Accesos por cada 100 hab', palette='viridis', ax=ax)
    ax.set_xlabel("Provincia")
    ax.set_ylabel("Accesos por cada 100 habitantes")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.write("### Variabilidad de Accesos por Provincia")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Provincia', y='Accesos por cada 100 hab', data=filtered_df_penetracion, palette='Set2', ax=ax)
    ax.set_xlabel("Provincia")
    ax.set_ylabel("Accesos por cada 100 habitantes")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
    st.dataframe(df_penetracion)

# Pagina Análisis de Accesos por Tecnología y Provincia
def pagina_accesos_tecnologia_localidad():
    st.header("📉 Analisis de Accesos por Tecnologia y Provincia")
    
    # Filtros
    tecnologias = st.sidebar.multiselect("Selecciona una o más tecnologías", df_accesos_tec["Tecnologia"].unique())
    provincias = st.sidebar.multiselect("Selecciona una o más provincias", df_accesos_tec["Provincia"].unique())
      
    # Filtrar datos según selección
    filtered_df_accesos = df_accesos_tec.copy()

    if provincias:
        filtered_df_accesos = filtered_df_accesos[filtered_df_accesos["Provincia"].isin(provincias)]
    if tecnologias:
        filtered_df_accesos = filtered_df_accesos[filtered_df_accesos["Tecnologia"].isin(tecnologias)]  

        st.write("### Vista Previa de los Datos de Accesos por Tecnología")
    st.dataframe(filtered_df_accesos.head())

    st.write("### Distribución de Tecnologías Usadas")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.countplot(data=filtered_df_accesos, x='Tecnologia', order=filtered_df_accesos['Tecnologia'].value_counts().index, palette='muted', ax=ax)
    ax.set_xlabel("Tecnología Usada")
    ax.set_ylabel("Cantidad de Registros")
    st.pyplot(fig)

    st.write("### Accesos por Tecnología y Provincia")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(data=filtered_df_accesos, x='Provincia', y='Accesos', hue='Tecnologia', palette='coolwarm', ax=ax)
    ax.set_xlabel("Provincia")
    ax.set_ylabel("Cantidad de Accesos")
    plt.xticks(rotation=90)
    st.pyplot(fig)

    st.write("### Boxplot de Accesos por Tecnología")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.boxplot(x='Tecnologia', y='Accesos', data=filtered_df_accesos, palette='Set2', ax=ax)
    ax.set_xlabel("Tecnología")
    ax.set_ylabel("Cantidad de Accesos")
    plt.xticks(rotation=90)
    st.pyplot(fig)
    
# Página Análisis de los Ingresos por Internet

def pagina_ingresos():
    st.header("📊 Analisis de los Ingresos")
    
    # Filtro de años
    años_seleccionados = st.sidebar.multiselect(
        'Selecciona los años que querés analizar',
        options=df_anual['Año'].unique(),
        default=df_anual['Año'].unique()
    )

    df_filtrado = df_anual[df_anual['Año'].isin(años_seleccionados)]

    # Gráfico de línea - Evolución temporal de ingresos anuales
    st.subheader('📈 Evolución de Ingresos Anuales')

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtrado, x='Año', y='Ingresos (miles de pesos)', marker='o', ax=ax)
    ax.set_title('Evolución de Ingresos Anuales')
    ax.set_xlabel('Año')
    ax.set_ylabel('Ingresos (miles de pesos)')
    ax.grid(True)
    st.pyplot(fig)

    # Boxplot - Distribución de ingresos anuales
    st.subheader('📦 Distribución de Ingresos Anuales')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df_filtrado['Ingresos (miles de pesos)'], color='skyblue', ax=ax)
    ax.set_title('Boxplot de Ingresos Anuales')
    ax.set_xlabel('Ingresos (miles de pesos)')
    st.pyplot(fig)

    # Histograma - Distribución de ingresos anuales
    st.subheader('📊 Histograma de Ingresos Anuales')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df_filtrado['Ingresos (miles de pesos)'], kde=True, color='skyblue', ax=ax, bins=15)
    ax.set_title('Distribución de Ingresos Anuales')
    ax.set_xlabel('Ingresos (miles de pesos)')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Tabla de datos
    st.subheader('📋 Datos Anuales Filtrados')
    st.dataframe(df_filtrado)

    # Métricas adicionales
    st.subheader('📊 Métricas Anuales')
    col1, col2, col3 = st.columns(3)

    col1.metric('Ingreso Promedio', f"${df_filtrado['Ingresos (miles de pesos)'].mean():,.0f} mil pesos")
    col2.metric('Ingreso Máximo', f"${df_filtrado['Ingresos (miles de pesos)'].max():,.0f} mil pesos")
    col3.metric('Ingreso Mínimo', f"${df_filtrado['Ingresos (miles de pesos)'].min():,.0f} mil pesos")

    # Análisis descriptivo
    st.subheader('📊 Análisis Descriptivo de los Ingresos Anuales')

    st.write(f"""
    - **Promedio Anual:** ${df_filtrado['Ingresos (miles de pesos)'].mean():,.0f} mil pesos.
    - **Desviación Estándar:** ${df_filtrado['Ingresos (miles de pesos)'].std():,.0f} mil pesos.
    - **Máximo Ingreso:** ${df_filtrado['Ingresos (miles de pesos)'].max():,.0f} mil pesos.
    - **Mínimo Ingreso:** ${df_filtrado['Ingresos (miles de pesos)'].min():,.0f} mil pesos.

    El gráfico de líneas muestra la evolución de los ingresos año a año. El boxplot nos permite identificar años atípicos (outliers) y el histograma muestra cómo se distribuyen los ingresos anuales.
    """)
    
def pagina_kpis():
    
    st.header("📊 Analisis KPIS")
    
    st.subheader("### KPI propuesto:Aumentar en un 2% el acceso al servicio de internet para el próximo trimestre, cada 100 hogares por provincia.")
    
    # Filtrar datos del último trimestre de 2023
    df_2023 = df_penetracion_hogares[df_penetracion_hogares["Año"] == 2023]
    df_ultimo_trim_2023 = df_2023[df_2023["Trimestre"] == df_2023["Trimestre"].max()]

    # Filtrar datos reales del último trimestre de 2024
    df_2024 = df_penetracion_hogares[df_penetracion_hogares["Año"] == 2024]
    df_ultimo_trim_2024 = df_2024[df_2024["Trimestre"] == df_2024["Trimestre"].max()]

    # Calcular la proyección con la fórmula KPI (aumento del 2%)
    df_ultimo_trim_2023["Predicción"] = df_ultimo_trim_2023["Accesos por cada 100 hogares"] * 1.02

    # Unir con los datos reales de 2024 para comparar
    df_pred = df_ultimo_trim_2023.merge(df_ultimo_trim_2024, on="Provincia", suffixes=("_Pred", "_Real"))

    # Calcular KPI
    df_pred["KPI (%)"] = ((df_pred["Accesos por cada 100 hogares_Real"] - df_pred["Predicción"]) / df_pred["Predicción"]) * 100

    # Mostrar datos calculados
    st.dataframe(df_pred[["Provincia", "Predicción", "Accesos por cada 100 hogares_Real", "KPI (%)"]])

    # Gráfico de comparación entre predicción y valor real
    fig = px.bar(df_pred, x="Provincia", y=["Predicción", "Accesos por cada 100 hogares_Real"], 
                title="Accesos a Internet: Predicción vs. Real",
                labels={"value": "Accesos por cada 100 hogares", "variable": "Tipo de Valor"},
                barmode="group")
    st.plotly_chart(fig)

    ### KPI Crecimiento Interanual

    # Filtrar el último año y trimestre disponibles
    ultimo_anio = df_penetracion['Año'].max()
    df_actual = df_penetracion[df_penetracion['Año'] == ultimo_anio]
    ultimo_trimestre = df_actual['Trimestre'].max()
    df_actual = df_actual[df_actual['Trimestre'] == ultimo_trimestre]

    # Obtener los datos del mismo trimestre pero del año anterior
    año_anterior = ultimo_anio - 1
    df_anterior = df_penetracion[(df_penetracion['Año'] == año_anterior) & (df_penetracion['Trimestre'] == ultimo_trimestre)]

    # Unir ambos dataframes por provincia
    df_kpi = df_actual.merge(df_anterior, on='Provincia', suffixes=('_actual', '_anterior'))

    # Calcular el KPI de crecimiento interanual
    df_kpi['KPI'] = ((df_kpi['Accesos por cada 100 hab_actual'] - df_kpi['Accesos por cada 100 hab_anterior']) / 
                    df_kpi['Accesos por cada 100 hab_anterior']) * 100

    # Gráfico de líneas para visualizar la evolución del KPI
    fig_kpi = px.line(df_kpi, x='Provincia', y='KPI', markers=True,
                    title='Crecimiento Interanual del Acceso a Internet (%)',
                    labels={'KPI': 'Crecimiento (%)', 'Provincia': 'Provincia'})
    fig_kpi.update_traces(line=dict(width=2))

    # Mostrar en el dashboard
    st.title('Análisis de KPI - Crecimiento Interanual')
    st.subheader('Comparación del acceso a internet respecto al año anterior')
    st.plotly_chart(fig_kpi, use_container_width=True)

    # Mostrar los datos en una tabla
    st.subheader('Datos del Crecimiento Interanual por Provincia')
    st.dataframe(df_kpi[['Provincia', 'Accesos por cada 100 hab_actual', 'Accesos por cada 100 hab_anterior', 'KPI']].rename(
    columns={'Accesos por cada 100 hab_actual': 'Accesos Actual', 'Accesos por cada 100 hab_anterior': 'Accesos Año Anterior', 'KPI': 'Crecimiento (%)'}
    ))

    ### KPI Penetracion de Fibra Optica por Provincia
    
    # Título del dashboard
    st.title("📊 KPI de Accesos por Fibra Óptica")

    # Filtros interactivos
    años_disponibles = sorted(df_totales["Año"].unique(), reverse=True)
    trimestres_disponibles = sorted(df_totales["Trimestre"].unique())

    años_seleccionados = st.multiselect("Selecciona uno o más Años", años_disponibles, default=[años_disponibles[0]])
    trimestres_seleccionados = st.multiselect("Selecciona uno o más Trimestres", trimestres_disponibles, default=[trimestres_disponibles[0]])

    # Filtrar datos por selección múltiple
    df_filtrado = df_totales[(df_totales["Año"].isin(años_seleccionados)) & (df_totales["Trimestre"].isin(trimestres_seleccionados))]

    # Calcular KPI (Porcentaje de Accesos por Fibra Óptica)
    df_filtrado["% Fibra Óptica"] = (df_filtrado["Fibra óptica"] / df_filtrado["Total"]) * 100

    # Mostrar tabla con los datos filtrados
    st.subheader("📌 Datos Filtrados")
    st.dataframe(df_filtrado[["Año", "Trimestre", "Periodo", "Fibra óptica", "Total", "% Fibra Óptica"]])

    # Crear gráfico de barras con Plotly
    fig = px.bar(df_filtrado, x="Periodo", y="% Fibra Óptica", color="Año", barmode="group",
                title="📊 % de Accesos por Fibra Óptica",
                labels={"Periodo": "Periodo", "% Fibra Óptica": "Porcentaje (%)"},
                text="% Fibra Óptica", height=500)

    st.plotly_chart(fig)

    # Mostrar el KPI principal en grande (promedio de todos los valores filtrados)
    kpi_valor = df_filtrado["% Fibra Óptica"].mean()
    st.metric(label="📌 Promedio de Accesos por Fibra Óptica (%)", value=f"{kpi_valor:.2f}%")

# Título general
st.title("📊 Dashboard de Accesos a Internet en Argentina")

# Selección de página
opcion_dashboard = st.sidebar.radio(
    "Selecciona una página", 
    ["Accesos a Internet por Tecnologia", "Penetracion de Internet", "Accesos por Tecnologia y Provincia", "Ingresos", "Analisis KPIS"]
)

# Mostrar la página seleccionada
if opcion_dashboard == "Accesos a Internet por Tecnologia":
    pagina_accesos_totales_tecnologia()
elif opcion_dashboard == "Penetracion de Internet":
    pagina_penetracion()
elif opcion_dashboard == "Accesos por Tecnologia y Provincia":
    pagina_accesos_tecnologia_localidad()
elif opcion_dashboard == "Ingresos":
    pagina_ingresos()
elif opcion_dashboard == "Analisis KPIS":
    pagina_kpis()
