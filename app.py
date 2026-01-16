import streamlit as st
import pandas as pd
from datetime import datetime
from gspread_pandas import Spread, conf

# Configuración
st.set_page_config(page_title="Sistema Producción Google", layout="centered")

# --- CONEXIÓN DIRECTA ---
# Usaremos una forma más robusta de conectar
def enviar_a_google(df_nuevo):
    try:
        # Aquí conectamos usando la URL que pusiste en Secrets
        url = st.secrets["gsheets"]["spreadsheet"]
        # Cargamos los datos actuales de la hoja
        df_actual = pd.read_csv(f"{url}/export?format=csv")
        # Unimos lo viejo con lo nuevo
        df_final = pd.concat([df_actual, df_nuevo], ignore_index=True)
        # NOTA: Para escribir usaremos un método más directo
        st.write("Datos listos para enviar...")
        return df_final
    except:
        return df_nuevo

# --- INTERFAZ ---
st.title("🚀 Registro de Producción")

with st.form("registro"):
    nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", JEAN", "JOSE"]) # Edita tus nombres aquí
    producto = st.text_input("Producto")
    cantidad = st.number_input("Cantidad", min_value=1)
    enviar = st.form_submit_button("Guardar en Google")

if enviar:
    nuevo = pd.DataFrame([{
        "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "Trabajador": nombre,
        "Producto": producto,
        "Cantidad": cantidad
    }])
    
    # Aquí es donde ocurre la magia de guardado
    # Por ahora, para evitar el error de permisos, 
    # te recomiendo usar el conector oficial de Streamlit así:
    from streamlit_gsheets import GSheetsConnection
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    try:
        existente = conn.read()
        actualizado = pd.concat([existente, nuevo], ignore_index=True)
        conn.update(data=actualizado)
        st.success("✅ ¡Guardado con éxito!")
    except Exception as e:
        st.error(f"Error de permisos: Asegúrate de que la hoja de Google esté compartida como EDITOR con cualquier persona que tenga el enlace.")