import streamlit as st
import pandas as pd
import os
from datetime import datetime
from io import BytesIO

# Configuración
st.set_page_config(page_title="Sistema Pro", layout="centered")

ARCHIVO_TRABAJADORES = "lista_trabajadores.csv"
ARCHIVO_PRODUCCION = "registro_produccion.csv"
PASSWORD_ADMIN = "1004"  # <--- CAMBIA TU CONTRASEÑA AQUÍ

def cargar_trabajadores():
    if os.path.isfile(ARCHIVO_TRABAJADORES):
        df = pd.read_csv(ARCHIVO_TRABAJADORES)
        return df['Nombre'].tolist()
    return []

# Menú lateral
st.sidebar.title("Navegación")
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Sistema Seguro Google", layout="centered")

# Conexión con Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar datos de trabajadores (los leeremos de una pestaña llamada 'Trabajadores')
# Nota: Para la primera vez, puedes definirlos manualmente o crear la pestaña
lista_trabajadores = ["Juan Perez", "Maria Garcia", "Luis Torres"] # Puedes editar esto

st.sidebar.title("Menú")
opcion = st.sidebar.selectbox("Ir a:", ["Registrar Producción", "Admin"])

if opcion == "Registrar Producción":
    st.title("📝 Registro en la Nube")
    
    with st.form("form_google"):
        nombre = st.selectbox("Tu Nombre", lista_trabajadores)
        prod = st.text_input("¿Qué hiciste?")
        cant = st.number_input("Cantidad", min_value=1)
        btn = st.form_submit_button("Enviar a Google Sheets")
        
    if btn:
        # Crear el nuevo registro
        nuevo_registro = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": prod,
            "Cantidad": cant
        }])
        
        # Leer datos actuales
        existente = conn.read(ttl=0)
        
        # Unir y actualizar
        actualizado = pd.concat([existente, nuevo_registro], ignore_index=True)
        conn.update(data=actualizado)
        
        st.success("✅ ¡Guardado en Google Sheets para siempre!")

elif opcion == "Admin":
    st.title("🔐 Panel de Control")
    clave = st.text_input("Contraseña", type="password")
    
    if clave == "1234":
        st.subheader("Datos en tiempo real")
        datos = conn.read(ttl=0)
        st.dataframe(datos)