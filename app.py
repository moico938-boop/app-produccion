import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Sistema Producción Pro", layout="wide")

st.title("🚀 Sistema de Registro de Producción")

# --- PEGA TU LINK AQUÍ ---
URL_HOJA = "https://docs.google.com/spreadsheets/d/1GwUdPBKicLHyN_FB9KcgT5FKOskP6yGRtVR9tCh_PVQ/edit?pli=1&gid=0#gid=0"

# Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("registro_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    with col2:
        producto = st.text_input("Producto")
    with col3:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
    
    enviar = st.form_submit_button("💾 GUARDAR REGISTRO")

if enviar:
    if not producto:
        st.warning("⚠️ Escribe el nombre del producto.")
    else:
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        try:
            # Leemos los datos actuales
            df_actual = conn.read(spreadsheet=URL_HOJA)
            
            # Unimos los datos
            df_actualizado = pd.concat([df_actual, nueva_fila], ignore_index=True)
            
            # Subimos la actualización
            conn.update(spreadsheet=URL_HOJA, data=df_actualizado)
            
            st.success(f"✅ ¡Guardado con éxito para {nombre}!")
            st.balloons()
            st.rerun() # Esto refresca la tabla de abajo automáticamente
        except Exception as e:
            st.error("❌ Error de permisos.")
            st.info("Sigue el paso del video: Google Sheets -> Compartir -> Cualquier persona -> EDITOR.")

st.divider()
st.subheader("📊 Últimos Registros Guardados")

try:
    datos = conn.read(spreadsheet=URL_HOJA)
    st.dataframe(datos.tail(10), use_container_width=True)
except:
    st.info("Esperando conexión con la hoja...")