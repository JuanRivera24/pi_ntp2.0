import streamlit as st
import pandas as pd
import requests
import google.generativeai as genai
import os

# --- Configuración de la Página ---
st.set_page_config(page_title="Diagnóstico del Sistema", page_icon="ախ", layout="wide")
st.title("ախ Diagnóstico del Sistema")
st.markdown("Esta página comprueba las conexiones a la API de Gemini, los archivos CSV locales y tu API central.")
st.markdown("---")

# --- TEST 1: Conexión a la API de Gemini ---
st.header("1. Prueba de Conexión con Google Gemini")

try:
    # Intenta leer la clave del archivo secrets.toml
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    
    # La prueba definitiva: listar los modelos disponibles
    st.info("Intentando listar los modelos de Gemini disponibles...")
    models_list = [m.name for m in genai.list_models()]
    
    st.success("✅ ¡ÉXITO! Conexión con la API de Google Gemini establecida.")
    with st.expander("Ver modelos encontrados en tu versión de la librería"):
        st.write(models_list)
        if 'models/gemini-pro' in models_list:
            st.success("El modelo 'gemini-pro' fue encontrado, ¡todo debería funcionar!")
        else:
            st.warning("ADVERTENCIA: El modelo 'gemini-pro' no aparece en la lista. Esto podría indicar que tu librería, aunque instalada, no es la más reciente. Intenta reinstalarla como último recurso.")

except Exception as e:
    st.error("❌ ERROR: No se pudo conectar con la API de Google Gemini.")
    st.error(f"Detalle del error: {e}")
    st.error("Verifica que tu API Key sea correcta y que el archivo `.streamlit/secrets.toml` esté en la raíz de tu proyecto.")

st.markdown("---")

# --- TEST 2: Carga de Archivos CSV Locales ---
st.header("2. Prueba de Carga de Archivos CSV")

try:
    st.info("Intentando leer los archivos desde la carpeta `data/`...")
    df_clientes = pd.read_csv("data/clientes.csv")
    df_citas = pd.read_csv("data/citas.csv")
    df_barberos = pd.read_csv("data/barberos.csv")
    df_sedes = pd.read_csv("data/sedes.csv")
    df_servicios = pd.read_csv("data/servicios.csv")
    
    st.success("✅ ¡ÉXITO! Todos los archivos CSV se cargaron correctamente.")
    st.write(f"- Clientes cargados: **{len(df_clientes)}**")
    st.write(f"- Citas cargadas: **{len(df_citas)}**")
    st.write(f"- Barberos cargados: **{len(df_barberos)}**")
    st.write(f"- Sedes cargadas: **{len(df_sedes)}**")
    st.write(f"- Servicios cargados: **{len(df_servicios)}**")

except FileNotFoundError as e:
    st.error(f"❌ ERROR: No se encontró el archivo CSV necesario: **{e.filename}**")
    st.error("Asegúrate de que todos los archivos CSV estén presentes en la carpeta `data`.")
except Exception as e:
    st.error(f"❌ ERROR: Ocurrió un problema al leer los archivos CSV.")
    st.error(f"Detalle del error: {e}")

st.markdown("---")

# --- TEST 3: Conexión a tu API Local ---
st.header("3. Prueba de Conexión a tu API Local (`index.js`)")

API_URL = "http://localhost:3001"
endpoints_a_probar = ["clientes", "citas", "barberos", "sedes", "servicios"]
errores = []

with st.spinner("Probando conexión con los endpoints..."):
    for endpoint in endpoints_a_probar:
        try:
            url = f"{API_URL}/{endpoint}"
            response = requests.get(url, timeout=5) # Timeout de 5 segundos
            response.raise_for_status()
            st.success(f"✅ Conexión exitosa con `/{endpoint}`. Se encontraron **{len(response.json())}** registros.")
        except Exception as e:
            st.error(f"❌ ERROR al conectar con `/{endpoint}`.")
            st.error(f"Detalle del error: {e}")
            errores.append(endpoint)

if not errores:
    st.success("✅ ¡ÉXITO! Todos los endpoints de la API local respondieron correctamente.")
else:
    st.error(f"**Resumen:** Falló la conexión con los siguientes endpoints: {', '.join(errores)}. Asegúrate de que tu `index.js` esté corriendo y que estas rutas estén definidas.")