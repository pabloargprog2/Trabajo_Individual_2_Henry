import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la página
st.set_page_config(page_title="Dashboard de Internet", layout="wide")

# Cargar datos
@st.cache_data
def cargar_datos():
    file_path = "dataset_internet.xlsx"
    df_accesos_tec = pd.read_excel(file_path, sheet_name='Accesos_tecnologia_localidad')
    return df_accesos_tec

df = cargar_datos()

# Sidebar - Filtros
st.sidebar.header("Filtros")
provincia = st.sidebar.selectbox("Seleccionar provincia", df["Provincia"].unique())
tecnologia = st.sidebar.selectbox("Seleccionar tecnología", df["Tecnologia"].unique())

df_filtrado = df[(df["Provincia"] == provincia) & (df["Tecnologia"] == tecnologia)]

# KPIs
st.title("Dashboard de Accesos a Internet")
st.metric("Total de Accesos", df_filtrado["Cantidad"].sum())

# Gráfico de barras por tecnología
st.subheader("Accesos por Tecnología")
fig, ax = plt.subplots()
sns.barplot(x="Tecnologia", y="Cantidad", data=df_filtrado, ax=ax)
st.pyplot(fig)

# Mapa de correlaciones
st.subheader("Correlaciones entre Variables")
fig_corr, ax_corr = plt.subplots()
sns.heatmap(df_filtrado.corr(), annot=True, cmap="coolwarm", ax=ax_corr)
st.pyplot(fig_corr)

# Boxplot para detectar outliers
st.subheader("Distribución de Accesos a Internet")
fig_box, ax_box = plt.subplots()
sns.boxplot(x=df_filtrado["Cantidad"], ax=ax_box)
st.pyplot(fig_box)

# Histograma de accesos
st.subheader("Histograma de Accesos a Internet")
fig_hist, ax_hist = plt.subplots()
sns.histplot(df_filtrado["Cantidad"], bins=50, kde=True, ax=ax_hist)
st.pyplot(fig_hist)

# Tabla de outliers
Q1 = df_filtrado["Cantidad"].quantile(0.25)
Q3 = df_filtrado["Cantidad"].quantile(0.75)
IQR = Q3 - Q1
limite_inferior = Q1 - 1.5 * IQR
limite_superior = Q3 + 1.5 * IQR
outliers = df_filtrado[(df_filtrado["Cantidad"] < limite_inferior) | (df_filtrado["Cantidad"] > limite_superior)]

st.subheader("Outliers Detectados")
st.dataframe(outliers)

# Gráfico de dispersión (scatter)
st.subheader("Relación entre Accesos y Otra Variable")
fig_scatter, ax_scatter = plt.subplots()
sns.scatterplot(x=df_filtrado["Cantidad"], y=df_filtrado["Velocidad"], ax=ax_scatter)
st.pyplot(fig_scatter)

# Gráfico de línea (tendencias en el tiempo)
st.subheader("Evolución de Accesos en el Tiempo")
if "Fecha" in df_filtrado.columns:
    df_time = df_filtrado.groupby("Fecha")["Cantidad"].sum().reset_index()
    fig_line, ax_line = plt.subplots()
    sns.lineplot(x=df_time["Fecha"], y=df_time["Cantidad"], ax=ax_line)
    st.pyplot(fig_line)
