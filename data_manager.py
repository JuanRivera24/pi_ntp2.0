import streamlit as st
import pandas as pd
import requests

API_URL = "http://localhost:8080"

# --- MÉTODO 1: Para Dashboard y Gestión de Citas (Usa la API de Java) ---

@st.cache_data
def obtener_datos_api(endpoint):
    """Función genérica para obtener datos de un endpoint de la API."""
    try:
        url = f"{API_URL}/{endpoint}"
        response = requests.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión al buscar '{endpoint}': {e}")
    except ValueError:
        st.error(f"La respuesta para '{endpoint}' no es un JSON válido.")
    return pd.DataFrame()

def cargar_datos_completos_api():
    """Carga todos los dataframes necesarios desde la API y renombra las columnas para compatibilidad."""
    df_clientes = obtener_datos_api("clientes")
    df_barberos = obtener_datos_api("barberos")
    df_servicios = obtener_datos_api("servicios")
    df_citas = obtener_datos_api("historial/citas")
    df_sedes = obtener_datos_api("sedes")

    # Capa de traducción para compatibilidad
    if not df_clientes.empty:
        df_clientes.rename(columns={'id': 'ID_Cliente', 'nombreCliente': 'Nombre_Cliente', 'apellidoCliente': 'Apellido_Cliente', 'telefono': 'Telefono', 'email': 'Email'}, inplace=True)
    if not df_barberos.empty:
        df_barberos['ID_Sede'] = df_barberos['sede'].apply(lambda x: x['id'] if isinstance(x, dict) else None)
        df_barberos.rename(columns={'id': 'ID_Barbero', 'nombreBarbero': 'Nombre_Barbero', 'apellidoBarbero': 'Apellido_Barbero'}, inplace=True)
    if not df_servicios.empty:
        df_servicios.rename(columns={'id': 'ID_Servicio', 'nombreServicio': 'Nombre_Servicio', 'precio': 'Precio', 'duracionMin': 'Duracion_min'}, inplace=True)
    if not df_citas.empty:
        df_citas.rename(columns={'id': 'ID_Cita', 'idCliente': 'ID_Cliente', 'idBarbero': 'ID_Barbero', 'idServicio': 'ID_Servicio', 'idSede': 'ID_Sede', 'fecha': 'Fecha', 'hora': 'Hora'}, inplace=True)
    if not df_sedes.empty:
        df_sedes.rename(columns={'id': 'ID_Sede', 'nombreSede': 'Nombre_Sede'}, inplace=True)
    
    return df_clientes, df_barberos, df_servicios, df_citas, df_sedes

def obtener_vista_citas_completa():
    """Obtiene datos de la API, realiza los merges Y DEVUELVE AMBOS DATAFRAMES NECESARIOS."""
    df_clientes, df_barberos, df_servicios, df_citas, df_sedes = cargar_datos_completos_api()
    
    if any(df.empty for df in [df_clientes, df_citas]):
        st.warning("No se pudieron cargar los datos de clientes o citas desde la API.")
        return pd.DataFrame(), pd.DataFrame() # Devuelve dos dataframes vacíos

    # Aseguramos que los IDs sean numéricos antes de unir
    for df in [df_clientes, df_citas, df_barberos, df_sedes, df_servicios]:
        for col in df.columns:
            if 'ID' in col:
                df[col] = pd.to_numeric(df[col], errors='coerce')

    df_clientes['Nombre_Completo_Cliente'] = df_clientes['Nombre_Cliente'] + ' ' + df_clientes['Apellido_Cliente']
    df_barberos['Nombre_Completo_Barbero'] = df_barberos['Nombre_Barbero'] + ' ' + df_barberos['Apellido_Barbero']
    
    df_vista = pd.merge(df_clientes, df_citas, on="ID_Cliente", how="left")
    df_vista = pd.merge(df_vista, df_sedes, on="ID_Sede", how="left")
    df_vista = pd.merge(df_vista, df_barberos, on="ID_Barbero", how="left")
    df_vista = pd.merge(df_vista, df_servicios, on="ID_Servicio", how="left")
    
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha'], errors='coerce')
    
    # --- CAMBIO IMPORTANTE: Devolvemos ambos dataframes ---
    return df_vista, df_sedes

# --- MÉTODO 2: Para Asistente IA (Usa los archivos CSV) ---
# (Esta parte no se ha modificado)
def cargar_datos_csv_locales():
    """Carga todos los dataframes desde los archivos CSV locales."""
    try:
        df_clientes = pd.read_csv("data/clientes.csv")
        df_barberos = pd.read_csv("data/barberos.csv")
        df_servicios = pd.read_csv("data/servicios.csv")
        df_citas = pd.read_csv("data/citas.csv")
        df_sedes = pd.read_csv("data/sedes.csv")
        return df_clientes, df_barberos, df_servicios, df_citas, df_sedes
    except FileNotFoundError as e:
        st.error(f"Error: No se encontró el archivo CSV: {e.filename}. Asegúrate de que los archivos estén en la carpeta 'data'.")
        return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())

def obtener_vista_citas_completa_csv():
    """Obtiene y une todos los datos desde los archivos CSV locales."""
    # ... (código existente sin cambios)
    pass