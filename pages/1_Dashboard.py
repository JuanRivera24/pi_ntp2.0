import streamlit as st
import plotly.express as px
import pandas as pd
# --- INICIO CAMBIO ---
# 1. Importar el data_manager correctamente para usar las nuevas funciones
import data_manager as dm 
# --- FIN CAMBIO ---
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
# Se mantiene igual, ya que data_manager ahora se encarga de todo
@st.cache_data
def cargar_datos_dashboard():
    # La función obtener_vista_citas_completa() ya nos trae los datos con la sede incluida
    df_vista_completa = dm.obtener_vista_citas_completa()
    df_productos = dm.cargar_productos_api()
    # --- INICIO CAMBIO ---
    # 2. Cargar también los datos de las sedes para el filtro
    _, _, _, _, df_sedes = dm.cargar_datos()
    return df_vista_completa, df_productos, df_sedes
    # --- FIN CAMBIO ---

df_vista_completa, df_productos, df_sedes = cargar_datos_dashboard()

# --- INICIO CAMBIO ---
# 3. Añadir el filtro de Sede en la parte superior del Dashboard
st.sidebar.header("Filtros del Dashboard")
# Crear una lista de opciones para el selectbox. Incluimos 'Todas'
lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_seleccionada = st.sidebar.selectbox("Selecciona una Sede", lista_sedes)

# 4. Filtrar el DataFrame principal según la selección
if sede_seleccionada == 'Todas':
    df_vista_filtrada = df_vista_completa.copy()
else:
    df_vista_filtrada = df_vista_completa[df_vista_completa['Nombre_Sede'] == sede_seleccionada]
# --- FIN CAMBIO ---


# --- Panel de Métricas Clave (KPIs) ---
st.header("Métricas Clave del Negocio")

# --- INICIO CAMBIO ---
# 5. Usar el nuevo DataFrame filtrado (df_vista_filtrada) para calcular las métricas
if not df_vista_filtrada.empty:
    total_ingresos = df_vista_filtrada['Precio'].sum()
    total_citas = len(df_vista_filtrada)
    # Usamos try-except por si no hay citas y .mode() da error
    try:
        servicio_popular = df_vista_filtrada['Nombre_Servicio'].mode().iloc[0]
    except IndexError:
        servicio_popular = "N/A"

    # Las columnas se mantienen igual
    col1, col2, col3 = st.columns(3, gap="large")
    with col1:
        st.metric(
            label=f"💰 Ingresos ({sede_seleccionada})",
            value=f"${total_ingresos:,.0f}",
            help="Suma de ingresos para la sede seleccionada."
        )
    with col2:
        st.metric(
            label=f"🗓️ Citas Registradas ({sede_seleccionada})",
            value=total_citas,
            help="Total de citas para la sede seleccionada."
        )
    with col3:
        st.metric(
            label=f"⭐ Servicio Popular ({sede_seleccionada})",
            value=servicio_popular,
            help="Servicio más reservado en la sede seleccionada."
        )
else:
    st.warning(f"No hay datos de citas para la sede '{sede_seleccionada}'.")
# --- FIN CAMBIO ---

st.markdown("---")

# --- Gráficos Interactivos con Plotly ---
st.header("Análisis Visual")
col_graf1, col_graf2 = st.columns(2, gap="large")

# Gráfico 1: Ingresos por Servicio (Gráfico de Torta - Pie Chart)
with col_graf1:
    st.subheader("Distribución de Ingresos por Servicio")
    # --- INICIO CAMBIO ---
    # 6. Usar también el DataFrame filtrado para los gráficos
    if not df_vista_filtrada.empty:
        ingresos_servicio = df_vista_filtrada.groupby('Nombre_Servicio')['Precio'].sum().reset_index()
        
        fig_pie = px.pie(
            ingresos_servicio,
            names='Nombre_Servicio',
            values='Precio',
            title=f'Proporción de Ingresos en {sede_seleccionada}',
            color_discrete_sequence=px.colors.sequential.Aggrnyl
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("No hay datos de ingresos para mostrar el gráfico.")
    # --- FIN CAMBIO ---

# Gráfico 2: Citas por Barbero
with col_graf2:
    st.subheader("Carga de Trabajo por Barbero")
    # --- INICIO CAMBIO ---
    # 7. Usar el DataFrame filtrado aquí también
    if not df_vista_filtrada.empty:
        # Aquí hay que tener cuidado: el nombre del barbero puede ser solo 'Nombre'
        # Asumiendo que `obtener_vista_citas_completa` ya une Nombre y Apellido
        # Si no, habría que ajustarlo en data_manager.py
        # Por ahora, asumimos que la columna se llama 'Nombre_Barbero'
        citas_barbero = df_vista_filtrada['Nombre'].value_counts().reset_index() # Suponiendo que la columna se llama 'Nombre' del barbero
        citas_barbero.columns = ['Barbero', 'Cantidad de Citas']
        
        fig_bar = px.bar(
            citas_barbero,
            x='Barbero',
            y='Cantidad de Citas',
            title=f'Citas por Barbero en {sede_seleccionada}',
            text='Cantidad de Citas',
            color='Barbero'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No hay datos para mostrar la carga de trabajo de los barberos.")
    # --- FIN CAMBIO ---


# --- Sección de Productos (Desde API) ---
# (Esta sección no necesita cambios, es independiente de las citas/sedes)
st.markdown("---")
st.header("📦 Inventario de Productos (Desde API)")
if not df_productos.empty:
    st.dataframe(df_productos, use_container_width=True)
else:
    st.error("🚨 Error: No se pudieron cargar los datos de productos desde la API.")