import streamlit as st
import pandas as pd
import os

# Configuración visual
st.set_page_config(page_title="Mi App de Personal", page_icon="👥")
st.title("Registro de Trabajadores")

# Formulario para ingresar datos
with st.form("registro_trabajador"):
    nombre = st.text_input("Nombre y Apellido")
    dni = st.text_input("DNI / Cédula")
    puesto = st.selectbox("Puesto", ["Operaciones", "Ventas", "Administración", "Logística"])
    fecha_ingreso = st.date_input("Fecha de Ingreso")
    
    boton_guardar = st.form_submit_button("Guardar Datos")

# Lógica para guardar la información
if boton_guardar:
    if nombre and dni:
        # Crear un diccionario con los datos
        datos = {
            "Nombre": [nombre],
            "Identificación": [dni],
            "Puesto": [puesto],
            "Fecha": [str(fecha_ingreso)]
        }
        df = pd.DataFrame(datos)
        
        # Guardar en un archivo Excel/CSV
        archivo = "trabajadores.csv"
        if not os.path.isfile(archivo):
            df.to_csv(archivo, index=False)
        else:
            df.to_csv(archivo, mode='a', header=False, index=False)
            
        st.success(f"✅ ¡Trabajador {nombre} guardado con éxito!")
    else:
        st.warning("⚠️ Por favor completa el Nombre y el DNI")

# Ver la lista de trabajadores
if st.checkbox("Ver lista de trabajadores"):
    if os.path.isfile("trabajadores.csv"):
        st.table(pd.read_csv("trabajadores.csv"))
    else:
        st.write("No hay datos registrados aún.")