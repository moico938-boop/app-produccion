import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Sistema de Producción Local", layout="wide")

st.title("🚀 Registro de Producción (Interno)")

# 2. CREAR LA BASE DE DATOS INTERNA
# Si es la primera vez que abrimos la app, creamos una tabla vacía
if 'base_datos' not in st.session_state:
    st.session_state.base_datos = pd.DataFrame(columns=["Fecha", "Trabajador", "Producto", "Cantidad"])

# --- FORMULARIO ---
with st.form("registro_interno"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    with col2:
        producto = st.text_input("Producto")
    with col3:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
    
    enviar = st.form_submit_button("💾 GUARDAR EN APP")

# --- LÓGICA PARA GUARDAR ---
if enviar:
    if not producto:
        st.warning("⚠️ Escribe el nombre del producto.")
    else:
        # Crear la fila nueva
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        # Guardar en la memoria de la app
        st.session_state.base_datos = pd.concat([st.session_state.base_datos, nueva_fila], ignore_index=True)
        st.success(f"✅ ¡Registro de {nombre} guardado en la tabla!")

# --- VISUALIZACIÓN DE LA TABLA ---
st.divider()
st.subheader("📊 Registros acumulados en esta sesión")

# Mostrar la tabla con todos los datos guardados
st.dataframe(st.session_state.base_datos, use_container_width=True)

# Botón opcional para borrar todo y empezar de cero
if st.button("🗑️ Borrar toda la tabla"):
    st.session_state.base_datos = pd.DataFrame(columns=["Fecha", "Trabajador", "Producto", "Cantidad"])
    st.rerun()