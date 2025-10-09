import streamlit as st
import sys
import os
import base64
import pandas as pd
import requests
import google.generativeai as genai
from streamlit import experimental_rerun # 1. IMPORTAMOS LA FUNCIÓN

# --- FUNCIÓN PARA CODIFICAR IMÁGENES ---
def get_image_as_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# --- FUNCIÓN DE DIAGNÓSTICO ---
def run_diagnostics():
    """Ejecuta y muestra los resultados de las pruebas del sistema directamente en la página."""
    st.markdown("Esta sección comprueba las conexiones a la API de Gemini, tu API central y los datasets externos.")
    st.markdown("---")

    # TEST 1: Conexión a la API de Gemini
    st.subheader("1. Prueba de Conexión con Google Gemini")
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        st.info("Intentando listar los modelos de Gemini disponibles...")
        models_list = [m.name for m in genai.list_models()]
        st.success("✅ ¡ÉXITO! Conexión con la API de Google Gemini establecida.")
        with st.expander("Ver modelos encontrados"):
            st.write(models_list)
            # Adaptado a un modelo estándar de Gemini
            if any('gemini-1.5-flash' in model_name for model_name in models_list):
                 st.success("Un modelo compatible ('gemini-1.5-flash') fue encontrado.")
            else:
                 st.warning("ADVERTENCIA: No se encontró un modelo 'gemini-1.5-flash'.")
    except Exception as e:
        st.error("❌ ERROR: No se pudo conectar con la API de Google Gemini.")
        st.error(f"Detalle: {e}")
        st.error("Verifica que tu API Key sea correcta y esté en el archivo `.streamlit/secrets.toml`.")

    st.markdown("---")

    # TEST 2: Conexión a tu API
    st.subheader("2. Prueba de Conexión a la API")
    if "API_URL" in st.secrets:
        API_URL = st.secrets["API_URL"]
        endpoints = ["clientes", "sedes", "servicios", "barberos", "citas-activas"] # Endpoints de ejemplo
        with st.spinner("Probando conexión con los endpoints de la API..."):
            all_successful = True
            for endpoint in endpoints:
                try:
                    response = requests.get(f"{API_URL}/{endpoint}", timeout=10)
                    response.raise_for_status()
                    st.success(f"✅ Conexión exitosa con `/{endpoint}` ({len(response.json())} registros).")
                except Exception as e:
                    st.error(f"❌ ERROR al conectar con `/{endpoint}`. Revisa que tu API esté desplegada y funcionando.")
                    st.expander("Ver detalle del error").error(e)
                    all_successful = False
            if all_successful:
                st.success("✅ ¡ÉXITO! Todos los endpoints de la API respondieron correctamente.")
    else:
        st.error("❌ ERROR: La variable `API_URL` no está configurada en los secretos de Streamlit.")


    st.markdown("---")

    # TEST 3: Prueba de Carga de Datasets Externos
    st.subheader("3. Prueba de Carga de Datasets Externos")
    datasets_externos = {
        "Nacional - Establecimientos de Belleza": "https://www.datos.gov.co/api/views/e27n-di57/rows.csv?accessType=DOWNLOAD",
    }
    with st.spinner("Probando la descarga de datasets de datos.gov.co..."):
        all_successful_external = True
        for nombre, url in datasets_externos.items():
            try:
                df = pd.read_csv(url, nrows=10)
                st.success(f"✅ Carga exitosa de '{nombre}'.")
            except Exception as e:
                st.error(f"❌ ERROR al cargar el dataset '{nombre}'.")
                st.expander("Ver detalle del error").error(e)
                all_successful_external = False
        if all_successful_external:
            st.success("✅ ¡ÉXITO! Todos los datasets externos se cargaron correctamente.")


# --- Rutas a las imágenes ---
ASSETS_DIR = "assets"
img_hero_path = os.path.join(ASSETS_DIR, "barber_hero.jpg")
img_logo_path = os.path.join(ASSETS_DIR, "Logo.png")
img_dev1_path = os.path.join(ASSETS_DIR, "1Desarrollador.png")
img_dev2_path = os.path.join(ASSETS_DIR, "2Desarrollador.png")
img_dev3_path = os.path.join(ASSETS_DIR, "3Desarrollador.png")

# Codificamos las imágenes
dev1_base64 = get_image_as_base64(img_dev1_path)
dev2_base64 = get_image_as_base64(img_dev2_path)
dev3_base64 = get_image_as_base64(img_dev3_path)

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Kingdom Barber | Inicio",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Contenido Principal ---
col1, col2 = st.columns([0.6, 0.4], gap="large")
with col1:
    if img_hero_path and os.path.exists(img_hero_path):
        st.image(img_hero_path, caption="El arte del cuidado masculino.", use_container_width=True)
    st.markdown(
        """<div style="text-align: center; margin-top: 20px;"><a href="https://pi-web2-0-two.vercel.app" target="_blank"><button style="background-color:#D4AF37; border:none; color:black; padding:12px 24px; text-align:center; text-decoration:none; display:inline-block; font-size:16px; border-radius:8px; cursor:pointer; font-weight:bold;">🌐 Visita nuestro sitio web</button></a></div>""",
        unsafe_allow_html=True
    )
with col2:
    st.markdown("<h1 style='text-align: left; color: #D4AF37;'>👑 Kingdom Barber</h1>", unsafe_allow_html=True)
    st.markdown("## Bienvenido al Panel de Gestión")
    st.markdown("Este es tu centro de control para administrar la barbería con eficiencia y estilo.")
    st.markdown("---")
    st.markdown("#### **¿Qué puedes hacer?**\n- **📊 Dashboard:** Analiza métricas clave.\n- **🗓️ Gestión de Citas:** Organiza tu agenda.\n- **🤖 Asistente IA:** Crea comunicaciones únicas.\n- **📂 Datasets:** Analiza datos reales.")

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    # --- INICIO DE LA CORRECCIÓN ---
    # Creamos un CSS para hacer el botón invisible
    st.markdown("""
        <style>
            div[data-testid="stButton.primary"] button {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
            div[data-testid="stButton.primary"] button:hover {
                background-color: transparent;
            }
            div[data-testid="stButton.primary"] button:active {
                background-color: transparent;
                border: none;
            }
        </style>
    """, unsafe_allow_html=True)

    # Creamos un botón "invisible" sobre la imagen
    if st.button("logo_recarga", type="primary", use_container_width=True):
        experimental_rerun()
    
    # Ponemos la imagen justo debajo del botón (visualmente se superponen)
    if img_logo_path and os.path.exists(img_logo_path):
        st.image(img_logo_path, width=100)
    # --- FIN DE LA CORRECCIÓN ---

    st.title("Menú de Navegación")
    st.success("Selecciona una página para comenzar.")
    st.markdown("---")

    # Botón para ejecutar el diagnóstico
    run_button = st.button("Ejecutar Diagnóstico del Sistema", use_container_width=True)

# --- Sección de Desarrolladores ---
st.markdown("<br><br><h2 style='text-align: center; color: #D4AF37;'>Conoce a los Desarrolladores</h2><hr style='border: 1px solid #D4AF37;'>", unsafe_allow_html=True)
st.markdown("""<style>.developer-card{background-color:#262730;border-radius:15px;padding:20px;text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center;align-items:center;}.developer-image{width:120px;height:160px;border-radius:10px;object-fit:cover;margin-bottom:15px;border:3px solid #D4AF37;}</style>""", unsafe_allow_html=True)
col_dev1, col_dev2, col_dev3 = st.columns(3, gap="large")
with col_dev1:
    if dev1_base64:
        st.markdown(f'<div class="developer-card"><img src="data:image/png;base64,{dev1_base64}" class="developer-image"><h4>Andrés Dario Vallejo Uchima</h4><p>📞 +57 319 3754588<br>📧 <a href="mailto:advallejouc@cesde.net">advallejouc@cesde.net</a><br>🐙 <a href="https://github.com/AndresVallejo1" target="_blank">AndresVallejo1</a></p></div>', unsafe_allow_html=True)
with col_dev2:
    if dev2_base64:
        st.markdown(f'<div class="developer-card"><img src="data:image/png;base64,{dev2_base64}" class="developer-image"><h4>Juan Manuel Rivera Restrepo</h4><p>📞 +57 302 3676712<br>📧 <a href="mailto:jmriverare@cesde.net">jmriverare@cesde.net</a><br>🐙 <a href="https://github.com/JuanRivera24" target="_blank">JuanRivera24</a></p></div>', unsafe_allow_html=True)
with col_dev3:
    if dev3_base64:
        st.markdown(f'<div class="developer-card"><img src="data:image/png;base64,{dev3_base64}" class="developer-image"><h4>Alejandro Urrego Cardona</h4><p>📞 +57 314 7692898<br>📧 <a href="mailto:aurregoc@cesde.net">aurregoc@cesde.net</a><br>🐙 <a href="https://github.com/AlejoU" target="_blank">AlejoU</a></p></div>', unsafe_allow_html=True)


# --- SECCIÓN DE DIAGNÓSTICO ---
if run_button:
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.title("Resultados del Diagnóstico del Sistema")
    run_diagnostics()