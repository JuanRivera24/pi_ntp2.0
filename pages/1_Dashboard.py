import streamlit as st
import plotly.express as px
import pandas as pd
import data_manager as dm
import locale

# --- 1. CONFIGURACIÓN INICIAL DE LA PÁGINA Y EL IDIOMA ---
try:
    # Intenta establecer el idioma a español para formatos de fecha y moneda
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Spanish')
    except locale.Error:
        st.warning("No se pudo establecer el local a español. Las fechas pueden aparecer en inglés.")

st.set_page_config(page_title="Dashboard | Kingdom Barber", page_icon="📊", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>📊 Dashboard General</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- 2. CARGA DE DATOS DESDE LA API A TRAVÉS DEL DATA_MANAGER ---
# Esta función llama a la API y procesa los datos. El resultado se guarda en caché.
@st.cache_data
def cargar_y_procesar_datos():
    """Carga y procesa todos los datos necesarios para el dashboard."""
    df_vista = dm.obtener_vista_citas_completa()
    df_sedes = dm.obtener_datos_api("sedes")
    return df_vista, df_sedes

df_vista_completa, df_sedes = cargar_y_procesar_datos()

# Si la carga de datos falla, se muestra un error y se detiene la ejecución.
if df_vista_completa.empty:
    st.error("No se pudieron cargar los datos desde la API. Asegúrate de que la API esté corriendo en http://localhost:3001.")
    st.stop()

# --- 3. FILTROS EN LA BARRA LATERAL ---
st.sidebar.header("Filtros del Dashboard")

lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_seleccionada = st.sidebar.selectbox("Selecciona una Sede", lista_sedes)

# Aplicar filtro de Sede
if sede_seleccionada == 'Todas':
    df_filtrado_parcial = df_vista_completa.copy()
else:
    df_filtrado_parcial = df_vista_completa[df_vista_completa['Nombre_Sede'] == sede_seleccionada]

# Crear listas para los siguientes filtros basadas en la selección anterior
lista_barberos = ['Todos'] + sorted(df_filtrado_parcial['Nombre_Completo_Barbero'].dropna().unique().tolist())
barbero_seleccionado = st.sidebar.selectbox("Selecciona un Barbero", lista_barberos)

# Aplicar filtro de Barbero
if barbero_seleccionado != 'Todos':
    df_filtrado_parcial = df_filtrado_parcial[df_filtrado_parcial['Nombre_Completo_Barbero'] == barbero_seleccionado]

lista_clientes = ['Todos'] + sorted(df_filtrado_parcial['Nombre_Completo_Cliente'].dropna().unique().tolist())
cliente_seleccionado = st.sidebar.selectbox("Selecciona un Cliente", lista_clientes)

# Aplicar filtro de Cliente para obtener el dataframe final
if cliente_seleccionado != 'Todos':
    df_vista_filtrada = df_filtrado_parcial[df_filtrado_parcial['Nombre_Completo_Cliente'] == cliente_seleccionado]
else:
    df_vista_filtrada = df_filtrado_parcial.copy()

# --- 4. CÁLCULO Y VISUALIZACIÓN DE MÉTRICAS CLAVE ---
st.header("Métricas Clave del Negocio")

# Filtramos solo las filas que son citas reales (tienen un ID_Cita)
df_citas_reales = df_vista_filtrada.dropna(subset=['ID_Cita'])

if not df_citas_reales.empty:
    total_ingresos = df_citas_reales['Precio'].sum()
    total_citas = len(df_citas_reales)
    servicio_popular = df_citas_reales['Nombre_Servicio'].mode().iloc[0]
    ingresos_por_barbero = df_citas_reales.groupby('Nombre_Completo_Barbero')['Precio'].sum()
    barbero_top = ingresos_por_barbero.idxmax() if not ingresos_por_barbero.empty else "N/A"

    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.metric(label="💰 Ingresos Totales", value=f"${total_ingresos:,.0f}")
    with col2:
        st.metric(label="🗓️ Citas Registradas", value=total_citas)
    with col3:
        st.metric(label="⭐ Servicio Popular", value=servicio_popular)
    with col4:
        st.metric(label="👑 Barbero Top (Ingresos)", value=barbero_top)
else:
    st.warning("No hay datos de citas para los filtros seleccionados.")

st.markdown("---")

# --- 5. VISUALIZACIONES Y GRÁFICOS ---
st.header("Análisis Visual")
col_graf1, col_graf2 = st.columns(2, gap="large")

with col_graf1:
    st.subheader("Distribución de Ingresos por Servicio")
    if not df_citas_reales.empty:
        ingresos_servicio = df_citas_reales.groupby('Nombre_Servicio')['Precio'].sum().reset_index()
        fig_pie = px.pie(ingresos_servicio, names='Nombre_Servicio', values='Precio',
                         title='Proporción de Ingresos', color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Sin datos de ingresos por servicio.")

with col_graf2:
    st.subheader("Carga de Trabajo por Barbero")
    if not df_citas_reales.empty:
        citas_barbero = df_citas_reales['Nombre_Completo_Barbero'].value_counts().reset_index()
        citas_barbero.columns = ['Barbero', 'Cantidad de Citas']
        fig_bar = px.bar(citas_barbero, x='Barbero', y='Cantidad de Citas', title='Citas por Barbero',
                         text='Cantidad de Citas', color='Barbero')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Sin datos de citas por barbero.")

st.markdown("<br>", unsafe_allow_html=True)
col_graf3, col_graf4 = st.columns(2, gap="large")

with col_graf3:
    st.subheader("Ingresos Generados por Barbero")
    if not df_citas_reales.empty and 'ingresos_por_barbero' in locals() and not ingresos_por_barbero.empty:
        df_ingresos_barbero = ingresos_por_barbero.reset_index()
        df_ingresos_barbero.columns = ['Barbero', 'Ingresos']
        fig_ingresos_barbero = px.bar(df_ingresos_barbero.sort_values('Ingresos', ascending=False),
                                      x='Barbero', y='Ingresos', title='Ingresos por Barbero',
                                      text='Ingresos', color='Barbero',
                                      color_discrete_sequence=px.colors.sequential.YlOrRd)
        fig_ingresos_barbero.update_traces(texttemplate='$%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig_ingresos_barbero, use_container_width=True)
    else:
        st.info("Sin datos de ingresos por barbero.")

with col_graf4:
    st.subheader("Evolución de Citas en el Tiempo")
    
    if not df_citas_reales.empty:
        agrupacion = st.radio(
            "Ver por:",
            ('Día', 'Semana', 'Mes'),
            horizontal=True,
            key='agrupacion_tiempo'
        )

        df_temp = df_citas_reales.copy()
        df_temp['Fecha_dt'] = pd.to_datetime(df_temp['Fecha'])

        if agrupacion == 'Día':
            df_agrupado = df_temp.groupby(df_temp['Fecha_dt'].dt.date).size().reset_index(name='Numero de Citas')
            df_agrupado.rename(columns={'Fecha_dt': 'Fecha'}, inplace=True)
        elif agrupacion == 'Semana':
            df_agrupado = df_temp.set_index('Fecha_dt').resample('W-Mon').size().reset_index(name='Numero de Citas')
            df_agrupado.rename(columns={'Fecha_dt': 'Fecha'}, inplace=True)
        else: # Mes
            df_agrupado = df_temp.set_index('Fecha_dt').resample('M').size().reset_index(name='Numero de Citas')
            df_agrupado.rename(columns={'Fecha_dt': 'Fecha'}, inplace=True)
            df_agrupado['Fecha'] = df_agrupado['Fecha'].dt.strftime('%Y-%m')

        fig_linea_tiempo = px.line(
            df_agrupado, 
            x='Fecha', 
            y='Numero de Citas',
            title=f'Citas por {agrupacion}', 
            markers=True,
            text='Numero de Citas'
        )
        fig_linea_tiempo.update_traces(textposition="top center")
        
        if not df_agrupado.empty:
            promedio_citas = df_agrupado['Numero de Citas'].mean()
            fig_linea_tiempo.add_hline(
                y=promedio_citas, 
                line_dash="dot",
                annotation_text=f"Promedio: {promedio_citas:.1f}",
                annotation_position="bottom right"
            )
        
        st.plotly_chart(fig_linea_tiempo, use_container_width=True)
    else:
        st.info("Sin datos para mostrar la evolución de citas.")