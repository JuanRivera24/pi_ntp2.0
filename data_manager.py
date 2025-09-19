import streamlit as st
import pandas as pd
import requests

# --- Caching de Datos ---
# @st.cache_data le dice a Streamlit que ejecute esta función solo una vez
# y guarde el resultado en caché. Si el código de la función no cambia,
# en las siguientes ejecuciones devolverá el resultado guardado sin leer los CSV de nuevo.

@st.cache_data
def cargar_datos():
    """Carga todos los dataframes desde los archivos CSV."""
    df_clientes = pd.read_csv("data/clientes.csv")
    df_barberos = pd.read_csv("data/barberos.csv")
    df_servicios = pd.read_csv("data/servicios.csv")
    df_citas = pd.read_csv("data/citas.csv")
    return df_clientes, df_barberos, df_servicios, df_citas

@st.cache_data
def cargar_productos_api():
    """Carga el catálogo de productos desde la API de Mockoon."""
    try:
        response = requests.get("http://localhost:3000/productos")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        # Si la API falla, devolvemos un DataFrame vacío para no romper la app.
        st.error(f"Error al conectar con la API de productos: {e}")
        return pd.DataFrame()

def obtener_vista_citas_completa():
    """Realiza los merges para tener una vista unificada de las citas."""
    df_clientes, df_barberos, df_servicios, df_citas = cargar_datos()
    
    df_vista = pd.merge(df_citas, df_clientes, on="ID_Cliente")
    df_vista = pd.merge(df_vista, df_barberos, on="ID_Barbero")
    df_vista = pd.merge(df_vista, df_servicios, on="ID_Servicio")
    
    # Convertir columna de fecha a formato datetime para poder filtrar
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha'])
    
    return df_vista