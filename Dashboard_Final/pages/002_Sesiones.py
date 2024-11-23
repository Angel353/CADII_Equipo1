import streamlit as st

st.title("Comparativa")
st.write("Dashboard de sesiones.")

# Pestañas para segmentación del tablero estadístico
tab1, tab2 = st.tabs([":bookmark_tabs: Temporales", ":bookmark_tabs: Zero Crossings"])

with tab1:
    st.header("Comparación entre sesiones temporal")
    st.dataframe({"Producto": ["A", "B", "C"] , "Ventas": [100, 150, 80]})
    
with tab2:
    st.header("Comparación de Pases por cero")
    st.dataframe({"Producto": ["A", "B", "C"] , "Ventas": [100, 150, 80]})