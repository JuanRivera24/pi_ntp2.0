import streamlit as st
import sys
import os
import base64

# --- FUNCIÓN PARA CODIFICAR IMÁGENES ---
def get_image_as_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        return None

# --- Rutas a las imágenes ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

img_hero_path = os.path.join(ASSETS_DIR, "barber_hero.jpg")
img_logo_path = os.path.join(ASSETS_DIR, "Logo.png")
img_dev1_path = os.path.join(ASSETS_DIR, "1Desarrollador.png")
img_dev2_path = os.path.join(ASSETS_DIR, "2Desarrollador.png")
img_dev3_path = os.path.join(ASSETS_DIR, "3Desarrollador.png")

# Codificamos las imágenes para usarlas en HTML
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
    st.image(img_hero_path, caption="El arte del cuidado masculino.", use_container_width=True)

    # --- Botón debajo de la imagen ---
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <a href="http://localhost:3000/" target="_blank">
                <button style="
                    background-color:#D4AF37;
                    border:none;
                    color:black;
                    padding:12px 24px;
                    text-align:center;
                    text-decoration:none;
                    display:inline-block;
                    font-size:16px;
                    border-radius:8px;
                    cursor:pointer;
                    font-weight:bold;
                ">
                    🌐 Visita nuestro sitio web
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown("<h1 style='text-align: left; color: #D4AF37;'>👑 Kingdom Barber</h1>", unsafe_allow_html=True)
    st.markdown("## Bienvenido al Panel de Gestión")
    st.markdown(
        """
        Este es tu centro de control para administrar la barbería con eficiencia y estilo. 
        Desde aquí, puedes acceder a todas las herramientas necesarias para llevar tu negocio al siguiente nivel.
        """
    )
    st.markdown("---")
    st.markdown(
        """
        #### **¿Qué puedes hacer?**
        - **📊 Dashboard:** Analiza métricas clave en tiempo real.
        - **🗓️ Gestión de Citas:** Organiza tu agenda y la de tus barberos.
        - **🤖 Asistente IA:** Crea comunicaciones únicas para tus clientes.
        
        Usa el menú lateral para navegar entre las secciones.
        """
    )

# --- Barra Lateral (Sidebar) ---
st.sidebar.image(img_logo_path, width=100) 
st.sidebar.title("Menú de Navegación")
st.sidebar.success("Selecciona una página para comenzar.")


# --- Estilos CSS para las Tarjetas de Desarrollador ---
st.markdown("""
<style>
.developer-card {
    background-color: #262730;
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    transition: 0.3s;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
.developer-card:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.4);
    transform: translateY(-5px);
}
.developer-image {
    width: 120px;
    height: 160px;
    border-radius: 10px;
    object-fit: cover;
    margin-bottom: 15px;
    border: 3px solid #D4AF37;
}
.developer-card h4 {
    margin-bottom: 10px;
    color: #FFFFFF;
}
.developer-card p {
    color: #a0a0a0;
    font-size: 0.9em;
}
.developer-card a {
    color: #D4AF37;
    text-decoration: none;
}
.developer-card a:hover {
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# --- Sección de Desarrolladores ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #D4AF37;'>Conoce a los Desarrolladores</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #D4AF37;'>", unsafe_allow_html=True)

col_dev1, col_dev2, col_dev3 = st.columns(3, gap="large")

# --- Tarjetas de Desarrollador con imágenes base64 ---
with col_dev1:
    if dev1_base64:
        st.markdown(
            f'''
            <div class="developer-card">
                <img src="data:image/png;base64,{dev1_base64}" class="developer-image">
                <h4>Andrés Dario Vallejo Uchima</h4>
                <p>
                    📞 +57 319 3754588 <br>
                    📧 <a href="mailto:advallejouc@cesde.net">advallejouc@cesde.net</a> <br>
                    🐙 <a href="https://github.com/AndresVallejo1" target="_blank">AndresVallejo1</a>
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )

with col_dev2:
    if dev2_base64:
        st.markdown(
            f'''
            <div class="developer-card">
                <img src="data:image/png;base64,{dev2_base64}" class="developer-image">
                <h4>Juan Manuel Rivera Restrepo</h4>
                <p>
                    📞 +57 302 3676712 <br>
                    📧 <a href="mailto:jmriverare@cesde.net">jmriverare@cesde.net</a> <br>
                    🐙 <a href="https://github.com/JuanRivera24" target="_blank">JuanRivera24</a>
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )

with col_dev3:
    if dev3_base64:
        st.markdown(
            f'''
            <div class="developer-card">
                <img src="data:image/png;base64,{dev3_base64}" class="developer-image">
                <h4>Alejandro Urrego Cardona</h4>
                <p>
                    📞 +57 314 7692898 <br>
                    📧 <a href="mailto:aurregoc@cesde.net">aurregoc@cesde.net</a> <br>
                    🐙 <a href="https://github.com/AlejoU" target="_blank">AlejoU</a>
                </p>
            </div>
            ''',
            unsafe_allow_html=True
        )
