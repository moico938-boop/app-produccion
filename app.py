import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Sistema Producción", layout="centered")

st.title("🚀 Registro de Producción")

# --- CONFIGURACIÓN DEL LINK ---
# REEMPLAZA ESTO CON TU LINK REAL
URL_HOJA = "TU_LINK_DE_GOOGLE_SHEETS_AQUI"

# Verificación de seguridad del link
if "docs.google.com" not in URL_HOJA:
    st.error("⚠️ El link de Google Sheets no es válido. Cópialo de la barra de direcciones de tu navegador.")
    st.stop()

# Conector
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("registro"):
    nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    producto = st.text_input("Producto (Nombre)")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    enviar = st.form_submit_button("Guardar en Google")

if enviar:
    if not producto:
        st.warning("⚠️ Escribe el nombre del producto.")
    else:
        # Fila nueva
        nuevo_registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Intentar leer y actualizar
            existente = conn.read(spreadsheet=URL_HOJA)
            actualizado = pd.concat([existente, nuevo_registro], ignore_index=True)
            conn.update(spreadsheet=URL_HOJA, data=actualizado)
            
            st.success(f"✅ ¡Guardado! {nombre} registró {cantidad} de {producto}")
            st.balloons()
        except Exception as e:
            st.error("❌ ERROR DE PERMISOS")
            st.info("Ve a tu Google Sheets -> Compartir -> Cambiar a 'Cualquier persona con el enlace' -> Cambiar a 'EDITOR'.")
            st.write(f"Detalle técnico: {e}")