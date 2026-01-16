import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Configuración visual
st.set_page_config(page_title="Registro en la Nube", page_icon="📝")

st.title("📝 Registro en la Nube")

# 2. PEGA TU LINK AQUÍ
# Recuerda: La hoja debe estar en "Cualquier persona con el enlace" y "EDITOR"
URL_HOJA = "TU_LINK_DE_GOOGLE_SHEETS_AQUI"

# 3. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Formulario de entrada
with st.form("registro"):
    nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    producto = st.text_input("Producto")
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    enviar = st.form_submit_button("Guardar en Google")

if enviar:
    if not producto:
        st.warning("⚠️ Por favor, escribe el nombre del producto.")
    else:
        # Creamos la nueva fila
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Leemos lo que ya existe
            datos_actuales = conn.read(spreadsheet=URL_HOJA)
            
            # Sumamos la nueva fila
            datos_nuevos = pd.concat([datos_actuales, nueva_fila], ignore_index=True)
            
            # Lo subimos todo de nuevo
            conn.update(spreadsheet=URL_HOJA, data=datos_nuevos)
            
            st.success(f"✅ ¡Registro de {nombre} guardado correctamente!")
        except Exception as e:
            st.error("❌ Error de permisos.")
            st.info("Asegúrate de que el Excel de Google esté compartido como 'EDITOR' con 'Cualquier persona con el enlace'.")