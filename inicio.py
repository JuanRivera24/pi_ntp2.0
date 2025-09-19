import streamlit as st

st.set_page_config(
    page_title="Kingdom Barber",
    page_icon="👑",
    layout="wide"
)

st.title("👑 Sistema de Gestión Kingdom Barber")
st.image("https://i.imgur.com/gL52m2a.jpeg", caption="El trono te espera.") # Reemplaza con una imagen tuya

st.markdown("""
### Bienvenido al panel de control de Kingdom Barber.

Este sistema te permite visualizar y gestionar las operaciones diarias de la barbería.

**Utiliza el menú de la izquierda para navegar por las diferentes secciones:**
- **Dashboard:** Visualiza métricas clave y el rendimiento del negocio.
- **Gestión de Citas:** Consulta, filtra y gestiona las citas programadas.
- **Asistente IA:** Utiliza inteligencia artificial para mejorar la comunicación con los clientes.

""")

st.sidebar.success("Selecciona una página para comenzar.")