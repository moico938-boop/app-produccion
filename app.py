import streamlit as st
import pandas as pd
from datetime import datetime

# 1. Configuración de la página
st.set_page_config(page_title="Sistema de Producción", layout="wide")

st.title("🚀 Registro de Producción (Control Total)")

# 2. INICIALIZAR LA TABLA INTERNA
if 'base_datos' not in st.session_state:
    st.session_state.base_datos = pd.DataFrame(columns=["Fecha", "Trabajador", "Producto", "Cantidad"])

# --- FORMULARIO DE REGISTRO ---
with st.container():
    st.subheader("Nuevo Registro")
    with st.form("registro_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            nombre = st.selectbox("Trabajador", ["ROGER", "ELIGIO", "CRISTIAN", "HENRRY", "JEAN", "JOSE"])
        with col2:
            producto = st.text_input("Producto")
        with col3:
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
        
        btn_guardar = st.form_submit_button("💾 GUARDAR")

if btn_guardar:
    if producto:
        nueva_fila = pd.DataFrame([{
            "Fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "Trabajador": nombre,
            "Producto": producto,
            "Cantidad": cantidad
        }])
        st.session_state.base_datos = pd.concat([st.session_state.base_datos, nueva_fila], ignore_index=True)
        st.success(f"✅ Registrado: {producto}")
    else:
        st.warning("⚠️ Escribe el producto")

# --- VISUALIZACIÓN Y BORRADO INDIVIDUAL ---
st.divider()
st.subheader("📊 Historial de Producción")

if not st.session_state.base_datos.empty:
    # Creamos una copia para mostrar
    df_mostrar = st.session_state.base_datos.copy()
    
    # Mostramos la tabla
    st.dataframe(df_mostrar, use_container_width=True)

    # SECCIÓN PARA BORRAR SOLO UNO
    st.write("---")
    st.write("🗑️ **Zona de corrección:**")
    fila_a_borrar = st.number_input("Escribe el número de fila que quieres borrar (empezando desde 0)", 
                                    min_value=0, 
                                    max_value=len(df_mostrar)-1, 
                                    step=1)
    
    if st.button("Eliminar solo esta fila"):
        # Borramos específicamente ese índice
        st.session_state.base_datos = st.session_state.base_datos.drop(fila_a_borrar).reset_index(drop=True)
        st.error(f"Fila {fila_a_borrar} eliminada.")
        st.rerun()
else:
    st.info("No hay datos registrados aún.")

# Botón de descarga para no perder la info al cerrar
if not st.session_state.base_datos.empty:
    csv = st.session_state.base_datos.to_csv(index=False).encode('utf-16')
    st.download_button(
        label="📥 Descargar Reporte del Día",
        data=csv,
        file_name=f'produccion_{datetime.now().strftime("%Y-%m-%d")}.csv',
        mime='text/csv',
    )