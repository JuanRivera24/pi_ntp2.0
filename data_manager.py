import streamlit as st
import pandas as pd
import requests
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@st.cache_data
def cargar_datos():
    """Carga todos los dataframes desde los archivos CSV, incluyendo las nuevas sedes."""
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
    Realiza los merges para tener una vista unificada de las citas, 
    asegurando que las columnas clave se mantengan y renombrando para evitar conflictos.
    """
    df_clientes, df_barberos, df_servicios, df_citas, df_sedes = cargar_datos()
    
    # --- INICIO CORRECCIÓN ---
    
    # 1. Renombrar columnas 'Nombre' y 'Apellido' para evitar conflictos antes de unir.
    df_clientes_renombrado = df_clientes.rename(columns={'Nombre': 'Nombre_Cliente', 'Apellido': 'Apellido_Cliente'})
    df_barberos_renombrado = df_barberos.rename(columns={'Nombre': 'Nombre_Barbero', 'Apellido': 'Apellido_Barbero'})
    
    # 2. Realizar los merges secuencialmente.
    # Unimos citas con clientes. df_citas ya tiene ID_Sede.
    df_vista = pd.merge(df_citas, df_clientes_renombrado, on="ID_Cliente")
    
    # Unimos con barberos. 
    # Aquí puede estar el problema. Si 'df_barberos' también tiene ID_Sede,
    # pandas crea ID_Sede_x y ID_Sede_y. Vamos a ser explícitos.
    # El ID_Sede de la cita es el que manda.
    df_vista = pd.merge(df_vista, df_barberos_renombrado, on="ID_Barbero", suffixes=('', '_barbero'))
    
    # Unimos con servicios
    df_vista = pd.merge(df_vista, df_servicios, on="ID_Servicio")
    
    # 3. Finalmente, unimos con sedes usando la columna 'ID_Sede' que viene de 'df_citas'.
    # Este merge ahora debería funcionar porque df_vista SÍ tiene la columna 'ID_Sede'.
    df_vista = pd.merge(df_vista, df_sedes, on="ID_Sede")
    
    # --- FIN CORRECCIÓN ---
    
    # Convertir columna de fecha a formato datetime
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha'])
    
    # Limpiamos columnas duplicadas de ID_Sede si es que se crearon (_barbero)
    if 'ID_Sede_barbero' in df_vista.columns:
        df_vista = df_vista.drop(columns=['ID_Sede_barbero'])
    
    return df_vista
