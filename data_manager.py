import streamlit as st
import pandas as pd
import requests
import sys
import os

# --- Esta línea es opcional si tus archivos están en la misma carpeta ---
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@st.cache_data
def cargar_datos():
    """Carga todos los dataframes desde los archivos CSV."""
    df_clientes = pd.read_csv("data/clientes.csv")
    df_barberos = pd.read_csv("data/barberos.csv")
    df_servicios = pd.read_csv("data/servicios.csv")
    df_citas = pd.read_csv("data/citas.csv")
    df_sedes = pd.read_csv("data/sedes.csv")
    return df_clientes, df_barberos, df_servicios, df_citas, df_sedes

@st.cache_data
def cargar_productos_api():
    """Carga el catálogo de productos desde la API de Mockoon."""
    try:
        response = requests.get("http://localhost:3000/productos")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de productos: {e}")
        return pd.DataFrame()

def obtener_vista_citas_completa():
    """
    Realiza los merges para tener una vista unificada de las citas y 
    crea columnas de nombre completo para clientes y barberos.
    """
    df_clientes, df_barberos, df_servicios, df_citas, df_sedes = cargar_datos()
    
    # 1. Crear las columnas de nombre completo.
    df_clientes['Nombre_Completo_Cliente'] = df_clientes['Nombre_Cliente'] + ' ' + df_clientes['Apellido_Cliente']
    df_barberos['Nombre_Completo_Barbero'] = df_barberos['Nombre_Barbero'] + ' ' + df_barberos['Apellido_Barbero']
    
    # 2. Realizar los merges en el orden correcto para evitar el KeyError.
    # Empezamos con citas y le añadimos sedes, que comparten ID_Sede.
    df_vista = pd.merge(df_citas, df_sedes, on="ID_Sede")
    
    # Ahora añadimos el resto de la información a la tabla ya combinada.
    df_vista = pd.merge(df_vista, df_clientes, on="ID_Cliente")
    df_vista = pd.merge(df_vista, df_barberos, on="ID_Barbero")
    df_vista = pd.merge(df_vista, df_servicios, on="ID_Servicio")
    
    # Convertir columna de fecha a formato datetime
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha'])
    
    return df_vista