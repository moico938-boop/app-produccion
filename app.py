import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Configuración de la página
st.set_page_config(page_title="Registro de Producción", layout="centered")

st.title("📝 Registro en la Nube")

# --- CONEXIÓN ---
# Pega aquí el link de tu hoja de Google
# Asegúrate de que esté como "EDITOR" para "Cualquier persona con el enlace"
URL_HOJA = "TU_LINK_DE_GOOGLE_SHEETS_AQUI"

conn = st.connection("gsheets", type=GSheetsConnection)

# --- FORMULARIO ---
with st.form("registro"):
    nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    producto = st.text_input("Producto")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    enviar = st.form_submit_button("Guardar en Google")

if enviar:
    if not producto:
        st.warning("⚠️ Escribe un producto.")
    elif URL_HOJA == "TU_LINK_DE_GOOGLE_SHEETS_AQUI":
        st.error("❌ Falta pegar el link de Google Sheets en el código.")
    else:
        # Fila nueva
        nuevo = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Leer datos actuales
            existente = conn.read(spreadsheet=URL_HOJA)
            
            # Unir y actualizar
            actualizado = pd.concat([existente, nuevo], ignore_index=True)
            conn.update(spreadsheet=URL_HOJA, data=actualizado)
            
            st.success(f"✅ ¡Guardado con éxito para {nombre}!")
            st.balloons()
        except Exception as e:
            st.error(f"Error de permisos: Revisa que la hoja sea pública como EDITOR.")