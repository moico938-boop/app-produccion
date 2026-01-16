import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Sistema de Producción", layout="centered")

# Archivos donde se guardará la información
ARCHIVO_TRABAJADORES = "lista_trabajadores.csv"
ARCHIVO_PRODUCCION = "registro_produccion.csv"

# Funciones auxiliares para cargar datos
def cargar_trabajadores():
    if os.path.isfile(ARCHIVO_TRABAJADORES):
        df = pd.read_csv(ARCHIVO_TRABAJADORES)
        return df['Nombre'].tolist()
    return []

# Menú lateral para navegar
menu = st.sidebar.selectbox("Selecciona una opción", ["Registrar Producción", "Admin: Gestión de Personal"])

# --- SECCIÓN 1: REGISTRO DE PRODUCCIÓN (Para los trabajadores) ---
if menu == "Registrar Producción":
    st.title("🏗️ Reporte de Producción Diaria")
    
    lista_nombres = cargar_trabajadores()
    
    if not lista_nombres:
        st.warning("Aún no hay trabajadores registrados. El administrador debe registrarlos primero.")
    else:
        with st.form("form_produccion", clear_on_submit=True):
            nombre = st.selectbox("Selecciona tu nombre", lista_nombres)
            producto = st.text_input("¿Qué produciste hoy?")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            
            enviado = st.form_submit_button("Enviar Reporte")
            
        if enviado:
            nuevo_dato = {
                "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")],
                "Trabajador": [nombre],
                "Producto": [producto],
                "Cantidad": [cantidad]
            }
            df = pd.DataFrame(nuevo_dato)
            if not os.path.isfile(ARCHIVO_PRODUCCION):
                df.to_csv(ARCHIVO_PRODUCCION, index=False)
            else:
                df.to_csv(ARCHIVO_PRODUCCION, mode='a', header=False, index=False)
            st.success(f"✅ ¡Gracias {nombre}! Datos guardados.")

# --- SECCIÓN 2: GESTIÓN DE PERSONAL (Para ti) ---
elif menu == "Admin: Gestión de Personal":
    st.title("👤 Registro de Nuevos Trabajadores")
    
    with st.form("form_admin"):
        nuevo_nombre = st.text_input("Nombre completo del nuevo trabajador")
        dni = st.text_input("DNI / Identificación")
        agregar = st.form_submit_button("Registrar Trabajador")
        
    if agregar and nuevo_nombre:
        nuevo_t = pd.DataFrame({"Nombre": [nuevo_nombre], "DNI": [dni]})
        if not os.path.isfile(ARCHIVO_TRABAJADORES):
            nuevo_t.to_csv(ARCHIVO_TRABAJADORES, index=False)
        else:
            nuevo_t.to_csv(ARCHIVO_TRABAJADORES, mode='a', header=False, index=False)
        st.success(f"👤 {nuevo_nombre} ha sido agregado al sistema.")

    # Mostrar listas
    st.divider()
    if st.checkbox("Ver lista de trabajadores registrados"):
        if os.path.isfile(ARCHIVO_TRABAJADORES):
            st.table(pd.read_csv(ARCHIVO_TRABAJADORES))
            
    if st.checkbox("Ver historial de producción"):
        if os.path.isfile(ARCHIVO_PRODUCCION):
            st.dataframe(pd.read_csv(ARCHIVO_PRODUCCION))