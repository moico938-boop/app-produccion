import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Configuración de la aplicación
st.set_page_config(page_title="Sistema de Producción Permanente", layout="wide")

st.title("📂 Sistema de Producción (Guardado en PC)")
st.info("Nota: Los datos se guardan automáticamente en tu computadora cada vez que presionas 'Guardar'.")

# --- LÓGICA DE ARCHIVO LOCAL ---
# Nombre del archivo que se creará en tu carpeta
NOMBRE_ARCHIVO = "base_datos_produccion.csv"

# Función para leer el archivo si ya existe
def cargar_datos_disco():
    if os.path.exists(NOMBRE_ARCHIVO):
        return pd.read_csv(NOMBRE_ARCHIVO)
    else:
        # Si el archivo no existe, crea una tabla vacía
        return pd.DataFrame(columns=["Fecha", "Trabajador", "Producto", "Cantidad"])

# Cargar los datos al inicio de la aplicación
if 'base_datos' not in st.session_state:
    st.session_state.base_datos = cargar_datos_disco()

# --- FORMULARIO DE REGISTRO ---
with st.form("formulario_registro", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
    with col2:
        producto = st.text_input("Producto / Tarea")
    with col3:
        cantidad = st.number_input("Cantidad", min_value=1, step=1)
    
    boton_guardar = st.form_submit_button("💾 GUARDAR REGISTRO")

# --- GUARDAR INFORMACIÓN ---
if boton_guardar:
    if producto:
        # Crear la fila nueva
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        
        # 1. Actualizar la tabla en la pantalla
        st.session_state.base_datos = pd.concat([st.session_state.base_datos, nueva_fila], ignore_index=True)
        
        # 2. GUARDAR FÍSICAMENTE EN EL DISCO DURO (El paso clave)
        st.session_state.base_datos.to_csv(NOMBRE_ARCHIVO, index=False)
        
        st.success(f"✅ Guardado correctamente en {NOMBRE_ARCHIVO}")
    else:
        st.warning("⚠️ Debes escribir el nombre del producto.")

# --- VISUALIZACIÓN Y CONTROL ---
st.divider()
st.subheader("📊 Historial Registrado")

# Mostrar la tabla actualizada
if not st.session_state.base_datos.empty:
    st.dataframe(st.session_state.base_datos, use_container_width=True)
    
    # OPCIÓN PARA BORRAR SOLO UN ERROR
    with st.expander("🛠️ Corregir o Borrar un registro"):
        fila_id = st.number_input("Número de fila a eliminar", min_value=0, max_value=len(st.session_state.base_datos)-1, step=1)
        if st.button("Eliminar Fila Seleccionada"):
            # Borrar de la memoria
            st.session_state.base_datos = st.session_state.base_datos.drop(fila_id).reset_index(drop=True)
            # Guardar el cambio en el archivo físico
            st.session_state.base_datos.to_csv(NOMBRE_ARCHIVO, index=False)
            st.error(f"Registro {fila_id} eliminado del disco.")
            st.rerun()
else:
    st.write("Aún no hay registros en el archivo.")

# Botón extra para abrir el archivo en Excel directamente
if not st.session_state.base_datos.empty:
    csv_data = st.session_state.base_datos.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar copia para Excel",
        data=csv_data,
        file_name=f"reporte_produccion_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime="text/csv"
    )