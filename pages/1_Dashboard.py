import streamlit as st
import plotly.express as px
import pandas as pd
import data_manager as dm 
import sys
import os

# Añade la carpeta raíz del proyecto a la ruta de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuración de la Página ---
st.set_page_config(page_title="Dashboard | Kingdom Barber", page_icon="📊", layout="wide")

# --- Título Principal ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>📊 Dashboard General</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Carga de Datos ---
# Usamos el decorador @st.cache_data en la función para que no se recargue innecesariamente
@st.cache_data
def cargar_datos():
    df_vista = dm.obtener_vista_citas_completa()
    df_productos = dm.cargar_productos_api()
    return df_vista, df_productos

df_vista, df_productos = cargar_datos()

# --- Panel de Métricas Clave (KPIs) ---
st.header("Métricas Clave del Negocio")

if not df_vista.empty:
    total_ingresos = df_vista['Precio'].sum()
    total_citas = len(df_vista)
    servicio_popular = df_vista['Nombre_Servicio'].mode().iloc[0]

    # Usamos columnas para un diseño más limpio
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.metric(
            label="💰 Ingresos Totales (Histórico)",
            value=f"${total_ingresos:,.0f}",
            help="Suma total de los ingresos de todas las citas completadas."
        )
    with col2:
        st.metric(
            label="🗓️ Total Citas Registradas",
            value=total_citas,
            help="Número total de citas registradas en el sistema."
        )
    with col3:
        st.metric(
            label="⭐ Servicio Más Popular",
            value=servicio_popular,
            help="El servicio que ha sido reservado más veces."
        )
else:
    st.warning("No hay datos de citas para mostrar las métricas.")

st.markdown("---")

# --- Gráficos Interactivos con Plotly ---
st.header("Análisis Visual")
col_graf1, col_graf2 = st.columns(2, gap="large")

# Gráfico 1: Ingresos por Servicio (Gráfico de Torta - Pie Chart)
with col_graf1:
    st.subheader("Distribución de Ingresos por Servicio")
    if not df_vista.empty:
        ingresos_servicio = df_vista.groupby('Nombre_Servicio')['Precio'].sum().reset_index()
        
        # Usamos Plotly para un gráfico más bonito e interactivo
        fig_pie = px.pie(
            ingresos_servicio,
            names='Nombre_Servicio',
            values='Precio',
            title='Proporción de Ingresos',
            color_discrete_sequence=px.colors.sequential.Aggrnyl # Paleta de colores elegante
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No hay datos de ingresos para mostrar el gráfico.")

# Gráfico 2: Citas por Barbero
with col_graf2:
    st.subheader("Carga de Trabajo por Barbero")
    if not df_vista.empty:
        citas_barbero = df_vista['Nombre_Barbero'].value_counts().reset_index()
        citas_barbero.columns = ['Barbero', 'Cantidad de Citas']
        
        # Gráfico de barras con Plotly
        fig_bar = px.bar(
            citas_barbero,
            x='Barbero',
            y='Cantidad de Citas',
            title='Número de Citas por Barbero',
            text='Cantidad de Citas', # Muestra el valor en la barra
            color='Barbero' # Colores diferentes para cada barbero
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No hay datos para mostrar la carga de trabajo de los barberos.")


# --- Sección de Productos (Desde API) ---
st.markdown("---")
st.header("📦 Inventario de Productos (Desde API)")
if not df_productos.empty:
    # Usamos st.dataframe para una tabla interactiva
    st.dataframe(df_productos, use_container_width=True)
else:
    st.error("🚨 Error: No se pudieron cargar los datos de productos desde la API.")