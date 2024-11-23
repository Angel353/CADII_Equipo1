import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout = "wide") # El tablero seteado en modo "wide"

st.title("Estadística")
st.write("Dashboard estadístico.")

df = pd.read_csv("Final/df.csv").drop(columns = "Unnamed: 0", axis = 1)

# Pestañas para segmentación del tablero estadístico
tab1, tab2 = st.tabs([":bookmark_tabs: Análisis Univariado", ":bookmark_tabs: Regresiones"])

# Sidebar para filtros
with st.sidebar:
    st.header("Filtros")
    
    # Listas únicas de las columnas
    pacientes = df['Paciente'].unique().tolist()
    sesiones = df['noSesion'].unique().tolist()
    ventaneos = df['Ventaneo'].unique().tolist()

    # Multiselects inicializados como vacíos
    selected_pacientes = st.multiselect("Selecciona Paciente(s):", pacientes, default=[])
    selected_sesiones = st.multiselect("Selecciona Sesión(es):", sesiones, default=[])
    selected_ventaneos = st.multiselect("Selecciona Ventaneo(s):", ventaneos, default=[])
    
    # Selectbox para seleccionar la variable en el eje Y
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns  # Solo columnas numéricas
    numeric_column_names = numeric_columns.tolist()
    

    univar = st.selectbox("Selecciona la variable para el análisis univariado:", numeric_columns, index = 0)

# Filtrar el dataframe según las selecciones (solo aplica filtros no vacíos)
filtered_df = df.copy()  # Trabajar sobre una copia para mantener el original intacto
if selected_pacientes:
    filtered_df = filtered_df[filtered_df['Paciente'].isin(selected_pacientes)]
if selected_sesiones:
    filtered_df = filtered_df[filtered_df['noSesion'].isin(selected_sesiones)]
if selected_ventaneos:
    filtered_df = filtered_df[filtered_df['Ventaneo'].isin(selected_ventaneos)]
    
    
numeric_data = filtered_df.select_dtypes(include=['float64', 'int64'])
    
    
with tab1:
    st.header("Dashboard de análisis Univariado")
    st.write(filtered_df.head())
    
    # Crear el gráfico de área apilada
    fig = px.bar(
        filtered_df, 
        x= "noSesion",  # Eje X con las sesiones
        y = univar,  # Eje Y 
        color="Paciente",  # Diferenciar por paciente
        title=f"Evolución de {univar} por Sesión",
        labels={"noSesion": "Sesión", univar: univar, "Paciente": "Paciente"},
        height=500,
        color_discrete_sequence=[
            "#89CFF0", "#00B9E8", "#246BCE", "#1F75FE", 
            "#B9D9EB", "#99FFFF", "#73C2FB", "#87D3F8"
        ]
    )

    # Personalización del layout: fondo negro y texto en blanco
    fig.update_layout(
        plot_bgcolor='black', # Fondo del gráfico en negro
        paper_bgcolor='black', # Fondo del área externa en negro
        title_font=dict(size=20, color='white'),  # Título en blanco
        font=dict(color='white'),  # Texto en blanco
        xaxis=dict(showgrid=False),  # Sin líneas internas
        yaxis=dict(showgrid=False),  # Sin líneas internas
        margin=dict(t=50, l=50, b=50, r=50),  # Márgenes para dar espacio
    )

    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)
    
    if univar:  # Variable del selectbox
        # Filtrando las correlaciones fuertes para la variable seleccionada
        heatMapUnique = abs(numeric_data.corr()[univar])
        heatMapUnique = heatMapUnique[heatMapUnique > 0.2].sort_values(ascending=False)
        heatMapUnique = heatMapUnique.to_frame()  # Convertir a DataFrame para graficar

        heatMapUnique.columns = ['Correlación']  # Renombrar la columna para el gráfico

        # Graficar el heatmap de la correlación con la variable seleccionada
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(
            heatMapUnique,  # Transpuesta para que los nombres de las variables estén en el eje X
            annot=True, 
            cmap='Blues', 
            cbar=True, 
            linewidths=0.5, 
            fmt=".2f",
            ax=ax
        )

        # Personalización del fondo negro y etiquetas en blanco
        ax.set_facecolor("black")  # Fondo del gráfico
        fig.patch.set_facecolor("black")  # Fondo exterior
        ax.set_title(f"Mapa de Calor de Correlaciones con '{univar}'", color="white")  # Título en blanco
        ax.tick_params(colors="white")  # Ejes en blanco
        ax.xaxis.label.set_color("white")  # Etiqueta del eje X en blanco
        ax.yaxis.label.set_color("white")  # Etiqueta del eje Y en blanco

        # Mostrar gráfico
        st.pyplot(fig)

        # Gráfico de Violín
        st.subheader(f"Gráfico de Violín para '{univar}'")

        # Crear el gráfico de violín
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.violinplot(
            data=filtered_df,
            y=univar,  # Variable en el eje Y
            x="Paciente",  # Agrupar por pacientes en el eje X
            palette="Blues",  # Escala de azules para el gráfico
            ax=ax
        )

        # Personalización del fondo negro y etiquetas en blanco
        ax.set_facecolor("black")  # Fondo del gráfico
        fig.patch.set_facecolor("black")  # Fondo exterior
        ax.set_title(f"Distribución de '{univar}' por Paciente", color="white")  # Título en blanco
        ax.tick_params(colors="white")  # Ticks en blanco
        ax.xaxis.label.set_color("white")  # Etiqueta del eje X en blanco
        ax.yaxis.label.set_color("white")  # Etiqueta del eje Y en blanco

        # Mostrar el gráfico en Streamlit
        st.pyplot(fig)
    
with tab2:
    st.header("Apartado de regresiones")
    st.dataframe({"Producto": ["A", "B", "C"] , "Ventas": [100, 150, 80]})