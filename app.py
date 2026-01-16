import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configuración de la aplicación
st.set_page_config(page_title="Registro de Producción", layout="centered")

st.title("📝 Registro de produccion")

# --- CONEXIÓN ---
# 1. PEGA TU LINK AQUÍ ENTRE LAS COMILLAS
URL_HOJA = "https://docs.google.com/spreadsheets/d/1GwUdPBKicLHyN_FB9KcgT5FKOskP6yGRtVR9tCh_PVQ/edit?pli=1&gid=0#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- INTERFAZ ---
with st.form("registro_produccion"):
    nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    producto = st.text_input("Producto")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    enviar = st.form_submit_button("Guardar en Google")

if enviar:
    if not producto:
        st.warning("⚠️ Por favor, ingresa un producto.")
    elif URL_HOJA == "https://docs.google.com/spreadsheets/d/1GwUdPBKicLHyN_FB9KcgT5FKOskP6yGRtVR9tCh_PVQ/edit?pli=1&gid=0#gid=0":
        st.error("❌ No has pegado el link de Google Sheets en el código.")
    else:
        # Fila nueva a insertar
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Leer datos actuales y combinar
            actual = conn.read(spreadsheet=URL_HOJA)
            df_final = pd.concat([actual, nueva_fila], ignore_index=True)
            
            # Subir actualización
            conn.update(spreadsheet=URL_HOJA, data=df_final)
            st.success(f"✅ ¡Registro guardado para {nombre}!")
            st.balloons()
        except Exception as e:
            st.error("❌ Error de permisos: Verifica que la hoja sea pública como EDITOR.")