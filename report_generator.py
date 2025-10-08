import streamlit as st
import pandas as pd
import requests

# NO HAY NINGUNA VARIABLE API_URL DEFINIDA AQUÍ ARRIBA

@st.cache_data
def obtener_vista_citas_completa():
    """
    Carga los datos de citas y sedes desde la API.
    """
    try:
        # Se define la API_URL DENTRO de la función, justo antes de usarla.
        API_URL = st.secrets["API_URL"]
        
        # Hacemos las llamadas a los endpoints necesarios
        citas_res = requests.get(f"{API_URL}/citas-activas")
        sedes_res = requests.get(f"{API_URL}/sedes")

        # Verificamos que las respuestas sean correctas (lanza un error si no lo son)
        citas_res.raise_for_status()
        sedes_res.raise_for_status()

        df_citas = pd.DataFrame(citas_res.json())
        df_sedes = pd.DataFrame(sedes_res.json())
        
        # --- Lógica de procesamiento de datos ---
        # (Esta sección es un ejemplo basado en tu código, ajústala si es necesario)
        
        # Convertir la columna de fecha a formato datetime
        if 'fechaInicio' in df_citas.columns:
            df_citas['Fecha'] = pd.to_datetime(df_citas['fechaInicio'])
            df_citas['Hora'] = df_citas['Fecha'].dt.strftime('%H:%M')
        else:
            # Crear columnas vacías si no hay datos para evitar errores posteriores
            df_citas['Fecha'] = pd.Series(dtype='datetime64[ns]')
            df_citas['Hora'] = pd.Series(dtype='object')

        # Renombrar columnas para consistencia (ejemplo)
        df_citas.rename(columns={
            'id': 'ID_Cita',
            'totalCost': 'Precio',
            'nombreSede': 'Nombre_Sede',
            'nombreCompletoBarbero': 'Nombre_Completo_Barbero',
            'clienteId': 'ID_Cliente',
            # Simulación de nombre de cliente (ajusta según tu lógica real)
            # 'nombreCompletoCliente': 'Nombre_Completo_Cliente' 
        }, inplace=True)

        # Si no tienes nombre de cliente, puedes crear una columna placeholder
        if 'Nombre_Completo_Cliente' not in df_citas.columns:
            df_citas['Nombre_Completo_Cliente'] = "Cliente " + df_citas.index.astype(str)

        if 'Nombre_Servicio' not in df_citas.columns:
            df_citas['Nombre_Servicio'] = "Servicio General"
            
        if 'Telefono' not in df_citas.columns:
            df_citas['Telefono'] = "N/A"

        # Renombrar columnas de sedes
        df_sedes.rename(columns={'id': 'ID_Sede', 'nombreSede': 'Nombre_Sede'}, inplace=True)
        
        return df_citas, df_sedes

    except requests.exceptions.RequestException as e:
        st.error(f"Error de conexión con la API: {e}")
        return pd.DataFrame(), pd.DataFrame()
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al procesar los datos: {e}")
        return pd.DataFrame(), pd.DataFrame()