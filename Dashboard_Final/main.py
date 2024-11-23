import streamlit as st

# Iniciar página: py -m streamlit run Final/main.py

def create_sidebar():
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "main.py"

    with st.sidebar:
        st.title("Haga clic en uno de nuestros tableros")
        st.write("1. Apartado Estadístico")
        st.write("2. Comparación entre sesiones")
        st.write("3. Comparación entre pacientes")
        

# Llama la función para inicializar la barra lateral
create_sidebar()

# Título de la página principal
st.title("Página Principal (Portada / Bienvenida)")
