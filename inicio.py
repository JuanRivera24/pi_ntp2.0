import streamlit as st
import sys
import os

# Añade la carpeta raíz del proyecto a la ruta de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuración de la Página (Mejorada) ---
st.set_page_config(
    page_title="Kingdom Barber | Inicio",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="expanded" # Asegura que la barra lateral esté visible por defecto
)

# --- Contenido Principal ---

# Dividimos la pantalla en dos columnas para un diseño más dinámico
col1, col2 = st.columns(
    [0.6, 0.4], # La columna 1 (imagen) ocupará el 60%, la columna 2 (texto) el 40%
    gap="large"  # Añadimos un espacio generoso entre las columnas
)

# --- Columna 1: Imagen Principal ---
with col1:
    st.image(
        "assets/barber_hero.jpg", # Asegúrate de tener esta imagen en tu carpeta 'assets'
        caption="El arte del cuidado masculino.",
        use_container_width=True # <--- Así queda corregido
    )

# --- Columna 2: Título y Descripción ---
with col2:
    st.markdown("<h1 style='text-align: left; color: #D4AF37;'>👑 Kingdom Barber</h1>", unsafe_allow_html=True)
    st.markdown("## Bienvenido al Panel de Gestión")
    st.markdown(
        """
        Este es tu centro de control para administrar la barbería con eficiencia y estilo. 
        Desde aquí, puedes acceder a todas las herramientas necesarias para llevar tu negocio al siguiente nivel.
        """
    )
    st.markdown("---") # Línea divisoria para separar visualmente
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
st.sidebar.image("assets/logo.png", width=100) 
st.sidebar.title("Menú de Navegación")
st.sidebar.success("Selecciona una página para comenzar.")