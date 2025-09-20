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
    Realiza los merges para tener una vista unificada, asegurando que todos los clientes
    estén presentes en el resultado final, incluso si no tienen citas.
    """
    df_clientes, df_barberos, df_servicios, df_citas, df_sedes = cargar_datos()
    
    # 1. Crear las columnas de nombre completo.
    df_clientes['Nombre_Completo_Cliente'] = df_clientes['Nombre_Cliente'] + ' ' + df_clientes['Apellido_Cliente']
    df_barberos['Nombre_Completo_Barbero'] = df_barberos['Nombre_Barbero'] + ' ' + df_barberos['Apellido_Barbero']
    
    # --- INICIO DE LA CORRECCIÓN ---

    # 2. Empezamos con el dataframe de clientes como base.
    # Usamos un 'left' merge para asegurarnos de que NINGÚN cliente se pierda,
    # aunque no tenga citas registradas.
    df_vista = pd.merge(df_clientes, df_citas, on="ID_Cliente", how="left")
    
    # 3. Ahora, unimos la información restante.
    # Para estos merges, si una cita no existe (NaN), los campos quedarán vacíos, lo cual es correcto.
    df_vista = pd.merge(df_vista, df_sedes, on="ID_Sede", how="left")
    df_vista = pd.merge(df_vista, df_barberos, on="ID_Barbero", how="left")
    df_vista = pd.merge(df_vista, df_servicios, on="ID_Servicio", how="left")
    
    # --- FIN DE LA CORRECCIÓN ---
    
    # Convertir columna de fecha a formato datetime
    # Usamos errors='coerce' para que no falle si hay fechas vacías (NaN)
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha'], errors='coerce')
    
    return df_vista


# --- FUNCIÓN PARA EJECUTAR EL DIAGNÓSTICO ---

def diagnosticar_datos():
    """
    Función de diagnóstico para imprimir el estado de los datos y los merges.
    No afecta al resto de la aplicación, solo sirve para que la probemos.
    """
    print("\n--- INICIANDO DIAGNÓSTICO ---")
    
    try:
        # 1. Cargar los datos crudos
        df_clientes, df_barberos, df_servicios, df_citas, df_sedes = cargar_datos()
        print(f"Paso 1: Se han cargado {len(df_clientes)} clientes desde clientes.csv.")
        print(f"Paso 2: Se han cargado {len(df_citas)} citas desde citas.csv.")
        
        # 2. Verificar los IDs
        clientes_con_citas = df_citas['ID_Cliente'].isin(df_clientes['ID_Cliente']).sum()
        print(f"Paso 3: De las {len(df_citas)} citas, {clientes_con_citas} tienen un ID_Cliente que SÍ existe en clientes.csv.")
        
        citas_perdidas = len(df_citas) - clientes_con_citas
        if citas_perdidas > 0:
            print(f"         🚨 ALERTA: Hay {citas_perdidas} citas con un ID_Cliente que NO existe en tu archivo de clientes. Estas citas se perderán en cualquier 'merge'.")

        # 3. Simular el merge final de la función obtener_vista_citas_completa()
        # Esto es una réplica exacta de la lógica que te dí en la última corrección.
        df_citas_enriquecidas = pd.merge(df_citas, df_sedes, on="ID_Sede", how="inner")
        df_citas_enriquecidas = pd.merge(df_citas_enriquecidas, df_barberos, on="ID_Barbero", how="inner")
        df_citas_enriquecidas = pd.merge(df_citas_enriquecidas, df_servicios, on="ID_Servicio", how="inner")
        
        df_vista_final = pd.merge(df_clientes, df_citas_enriquecidas, on="ID_Cliente", how="left")
        
        clientes_unicos_finales = df_vista_final['ID_Cliente'].nunique()
        print(f"Paso 4: Después de hacer todos los merges, el dataframe final tiene {clientes_unicos_finales} clientes únicos.")

        if clientes_unicos_finales == len(df_clientes):
            print("         ✅ ÉXITO: El número de clientes en el resultado final coincide con el número de clientes en tu CSV. El código de merge es correcto.")
        else:
            print(f"         🚨 PROBLEMA: Algo en los merges está haciendo que se pierdan clientes. El resultado tiene {len(df_clientes) - clientes_unicos_finales} clientes menos de los esperados.")
            
        print("--- FIN DEL DIAGNÓSTICO ---\n")

    except Exception as e:
        print(f"Ocurrió un error durante el diagnóstico: {e}")

# --- PARA EJECUTAR EL DIAGNÓSTICO, AÑADE ESTA LÍNEA AL FINAL DE TODO ---
if __name__ == "__main__":
    diagnosticar_datos()
