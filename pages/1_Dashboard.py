import streamlit as st
import plotly.express as px
import pandas as pd
import data_manager as dm 
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Dashboard | Kingdom Barber", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>📊 Dashboard General</h1>", unsafe_allow_html=True)
st.markdown("---")

@st.cache_data
def cargar_datos_dashboard():
    # La función obtener_vista_citas_completa() ya nos trae la columna 'Nombre_Completo_Barbero'
    df_vista_completa = dm.obtener_vista_citas_completa()
    df_productos = dm.cargar_productos_api()
    _, _, _, _, df_sedes = dm.cargar_datos()
    return df_vista_completa, df_productos, df_sedes

df_vista_completa, df_productos, df_sedes = cargar_datos_dashboard()

st.sidebar.header("Filtros del Dashboard")
lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_seleccionada = st.sidebar.selectbox("Selecciona una Sede", lista_sedes)

if sede_seleccionada == 'Todas':
    df_vista_filtrada = df_vista_completa.copy()
else:
    df_vista_filtrada = df_vista_completa[df_vista_completa['Nombre_Sede'] == sede_seleccionada]


st.header("Métricas Clave del Negocio")

if not df_vista_filtrada.empty:
    total_ingresos = df_vista_filtrada['Precio'].sum()
    total_citas = len(df_vista_filtrada)
    try:
        servicio_popular = df_vista_filtrada['Nombre_Servicio'].mode().iloc[0]
    except IndexError:
        servicio_popular = "N/A"

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

st.markdown("---")

st.header("Análisis Visual")
col_graf1, col_graf2 = st.columns(2, gap="large")

with col_graf1:
    st.subheader("Distribución de Ingresos por Servicio")
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

# Gráfico 2: Citas por Barbero
with col_graf2:
    st.subheader("Carga de Trabajo por Barbero")
    if not df_vista_filtrada.empty:
        # --- INICIO DE LA CORRECCIÓN ---
        # 1. Usar la nueva columna 'Nombre_Completo_Barbero' creada en data_manager.py
        citas_barbero = df_vista_filtrada['Nombre_Completo_Barbero'].value_counts().reset_index()
        # 2. Renombrar las columnas para el gráfico
        citas_barbero.columns = ['Barbero', 'Cantidad de Citas']
        # --- FIN DE LA CORRECCIÓN ---
        
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


st.markdown("---")
st.header("📦 Inventario de Productos (Desde API)")
if not df_productos.empty:
    st.dataframe(df_productos, use_container_width=True)
else:
    st.error("🚨 Error: No se pudieron cargar los datos de productos desde la API.")