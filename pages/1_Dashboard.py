import streamlit as st
import plotly.express as px
import pandas as pd
import data_manager as dm

# --- 2. Configuración de la Página ---
st.set_page_config(
    page_title="Dashboard | Kingdom Barber",
    page_icon="📊",
    layout="wide"
)

# --- 3. Título Principal ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>📊 Dashboard General</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 4. Carga de Datos (con caché) ---
# Usamos el decorador de Streamlit para cachear los datos y mejorar el rendimiento.
@st.cache_data
def cargar_datos_dashboard():
    df_vista = dm.obtener_vista_citas_completa()
    df_productos = dm.cargar_productos_api()
    return df_vista, df_productos

df_vista, df_productos = cargar_datos_dashboard()

# --- 5. Lógica Principal del Dashboard ---
# Se verifica si hay datos de citas para mostrar. Si no, se muestra un aviso y se detiene la ejecución.
if df_vista.empty:
    st.warning("No hay datos de citas disponibles para generar el dashboard.")
    st.stop() # Detiene la ejecución del script para no mostrar secciones vacías

# Si llegamos aquí, es porque df_vista tiene datos.

# --- Métricas Clave (KPIs) ---
st.header("Métricas Clave del Negocio")

total_ingresos = df_vista['Precio'].sum()
total_citas = len(df_vista)
servicio_popular = df_vista['Nombre_Servicio'].mode().iloc[0]

col1, col2, col3 = st.columns(3, gap="large")
with col1:
    st.metric(
        label="💰 Ingresos Totales",
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

st.markdown("---")

# --- Gráficos Interactivos ---
st.header("Análisis Visual")
col_graf1, col_graf2 = st.columns(2, gap="large")

# Gráfico 1: Distribución de Ingresos por Servicio
with col_graf1:
    st.subheader("Distribución de Ingresos por Servicio")
    ingresos_servicio = df_vista.groupby('Nombre_Servicio')['Precio'].sum().reset_index()
    
    fig_pie = px.pie(
        ingresos_servicio,
        names='Nombre_Servicio',
        values='Precio',
        title='Proporción de Ingresos',
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

# Gráfico 2: Carga de Trabajo por Barbero
with col_graf2:
    st.subheader("Carga de Trabajo por Barbero")
    citas_barbero = df_vista['Nombre_Barbero'].value_counts().reset_index()
    citas_barbero.columns = ['Barbero', 'Cantidad de Citas']
    
    fig_bar = px.bar(
        citas_barbero,
        x='Barbero',
        y='Cantidad de Citas',
        title='Número de Citas por Barbero',
        text='Cantidad de Citas',
        color='Barbero'
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Sección de Productos (Desde API) ---
st.markdown("---")
st.header("📦 Inventario de Productos")
if not df_productos.empty:
    st.dataframe(df_productos, use_container_width=True)
else:
    st.error("🚨 No se pudieron cargar los datos de productos desde la API.")