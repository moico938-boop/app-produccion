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
menu = st.sidebar.selectbox("Ir a:", ["Registrar Producción", "Admin: Gestión y Reportes"])

# --- SECCIÓN 1: TRABAJADORES ---
if menu == "Registrar Producción":
    st.title("🏗️ Reporte Diario")
    lista = cargar_trabajadores()
    
    if not lista:
        st.warning("⚠️ No hay trabajadores. Avisa a tu jefe.")
    else:
        with st.form("prod", clear_on_submit=True):
            nombre = st.selectbox("Selecciona tu nombre", lista)
            producto = st.text_input("Producto/Tarea")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            if st.form_submit_button("Enviar Reporte"):
                nuevo = pd.DataFrame({
                    "Fecha": [datetime.now().strftime("%d/%m/%Y %H:%M")],
                    "Trabajador": [nombre],
                    "Producto": [producto],
                    "Cantidad": [cantidad]
                })
                nuevo.to_csv(ARCHIVO_PRODUCCION, mode='a', index=False, header=not os.path.isfile(ARCHIVO_PRODUCCION))
                st.success(f"✅ ¡Hecho, {nombre}!")

# --- SECCIÓN 2: ADMIN (CON SEGURIDAD Y EXCEL) ---
elif menu == "Admin: Gestión y Reportes":
    st.title("🔐 Panel de Control")
    
    # Bloque de seguridad
    clave = st.text_input("Introduce la contraseña de administrador", type="password")
    
    if clave == PASSWORD_ADMIN:
        st.success("Acceso concedido")
        
        # Registro de personal
        with st.expander("➕ Registrar Nuevo Trabajador"):
            with st.form("admin_form", clear_on_submit=True):
                n_nom = st.text_input("Nombre completo")
                n_dni = st.text_input("DNI")
                if st.form_submit_button("Guardar"):
                    pd.DataFrame({"Nombre":[n_nom], "DNI":[n_dni]}).to_csv(ARCHIVO_TRABAJADORES, mode='a', index=False, header=not os.path.isfile(ARCHIVO_TRABAJADORES))
                    st.rerun()

        st.divider()
        st.subheader("📊 Historial de Producción")

        if os.path.isfile(ARCHIVO_PRODUCCION):
            df_final = pd.read_csv(ARCHIVO_PRODUCCION)
            st.dataframe(df_final)

            # --- BOTÓN PARA DESCARGAR EXCEL ---
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df_final.to_excel(writer, index=False, sheet_name='Produccion')
            
            st.download_button(
                label="📥 Descargar todo en Excel",
                data=output.getvalue(),
                file_name=f"Produccion_{datetime.now().strftime('%Y-%m-%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("No hay datos de producción todavía.")
    elif clave != "":
        st.error("❌ Contraseña incorrecta")