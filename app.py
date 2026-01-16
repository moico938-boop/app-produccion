import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la página
st.set_page_config(page_title="Sistema de Producción Pro", layout="wide")

st.title("🚀 Sistema de Registro de Producción")

# --- CONFIGURACIÓN DEL ENLACE ---
# PEGA AQUÍ TU LINK DE GOOGLE SHEETS
URL_HOJA = "https://docs.google.com/spreadsheets/d/1GwUdPBKicLHyN_FB9KcgT5FKOskP6yGRtVR9tCh_PVQ/edit?pli=1&gid=0#gid=0"

# 2. Conexión a la base de datos
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULARIO EN LA PARTE SUPERIOR ---
with st.form("registro_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    with col2:
        producto = st.text_input("Producto")
    with col3:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
    
    enviar = st.form_submit_button("💾 GUARDAR REGISTRO")

# --- LÓGICA DE GUARDADO ---
if enviar:
    if not producto:
        st.warning("⚠️ Escribe el nombre del producto.")
    elif "docs.google.com" not in URL_HOJA:
        st.error("❌ Falta el link de Google Sheets en el código.")
    else:
        nuevo_dato = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Leer, unir y actualizar
            actual = conn.read(spreadsheet=URL_HOJA)
            df_final = pd.concat([actual, nuevo_dato], ignore_index=True)
            conn.update(spreadsheet=URL_HOJA, data=df_final)
            
            st.success(f"✅ ¡Hecho! Registro guardado para {nombre}")
            st.balloons()
        except Exception as e:
            st.error("❌ Error de permisos o conexión.")

# --- MEJORA: VISUALIZACIÓN DE DATOS ---
st.divider()
st.subheader("📊 Últimos Registros Guardados")

try:
    # Mostramos los últimos 10 registros de la hoja
    datos_visualizar = conn.read(spreadsheet=URL_HOJA)
    if not datos_visualizar.empty:
        # Los ordenamos para que el más nuevo salga arriba
        st.dataframe(datos_visualizar.tail(10), use_container_width=True)
    else:
        st.info("La hoja está vacía actualmente.")
except:
    st.info("Conecta el link de Google Sheets para ver el historial.")