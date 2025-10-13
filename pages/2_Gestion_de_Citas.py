import streamlit as st
import pandas as pd
import data_manager as dm
from datetime import datetime

st.set_page_config(page_title="Gestión de Citas | Kingdom Barber", page_icon="🗓️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🗓️ Gestión de Citas</h1>", unsafe_allow_html=True)
st.markdown("### Filtra, busca y gestiona todas las citas de la barbería.")
st.markdown("---")

df_vista, df_sedes = dm.obtener_vista_citas_completa()

if df_vista.empty:
    st.error("No se pudieron cargar los datos de citas desde la API. Asegúrate de que la API de Java esté corriendo.")
    st.stop()

st.sidebar.header("🔍 Filtros Avanzados")

# --- LÓGICA DE FILTRADO SECUENCIAL Y DINÁMICO ---

# Creamos una copia maestra para irla reduciendo
df_filtrado = df_vista.copy()

# PASO 1: Filtrar por Sede
lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_sel = st.sidebar.selectbox("Filtrar por Sede:", options=lista_sedes)
if sede_sel != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Sede'] == sede_sel]

# PASO 2: Filtrar por Barbero (las opciones se basan en el resultado del filtro de sede)
opciones_barbero = ["Todos"] + sorted(list(df_filtrado['Nombre_Completo_Barbero'].dropna().unique()))
barbero_sel = st.sidebar.selectbox("Filtrar por Barbero:", options=opciones_barbero)
if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Barbero'] == barbero_sel]

# PASO 3: Filtrar por Cliente (las opciones se basan en el resultado de los filtros de sede Y barbero)
opciones_cliente = ["Todos"] + sorted(list(df_filtrado['Nombre_Completo_Cliente'].dropna().unique()))
cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", options=opciones_cliente)
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Cliente'] == cliente_sel]

# PASO 4: Filtrar por Fecha (el rango de fechas se basa en el resultado de TODOS los filtros anteriores)
fechas_validas = df_filtrado['Fecha'].dropna()
min_fecha = fechas_validas.min().date() if not fechas_validas.empty else datetime.now().date()
max_fecha = fechas_validas.max().date() if not fechas_validas.empty else datetime.now().date()

fecha_sel = st.sidebar.date_input(
    "Filtrar por Rango de Fecha:",
    value=(min_fecha, max_fecha),
    min_value=min_fecha,
    max_value=max_fecha,
    key="date_range_picker_gestion"
)

if len(fecha_sel) == 2:
    fecha_inicio, fecha_fin = fecha_sel
    # Aseguramos que la columna 'Fecha' no tenga nulos antes de comparar
    df_filtrado = df_filtrado.dropna(subset=['Fecha'])
    df_filtrado = df_filtrado[(df_filtrado['Fecha'].dt.date >= fecha_inicio) & (df_filtrado['Fecha'].dt.date <= fecha_fin)]

# --- FIN DE LA LÓGICA DE FILTRADO ---

df_citas_reales = df_filtrado.dropna(subset=['ID_Cita'])

st.header(f"Resultados: {len(df_citas_reales)} citas encontradas")

if df_citas_reales.empty:
    st.info("No se encontraron citas que coincidan con los filtros seleccionados.")
else:
    total_ingresos_filtrado = df_citas_reales['Precio'].sum()
    st.metric(
        label=f"💰 Ingresos para esta selección",
        value=f"${total_ingresos_filtrado:,.0f}"
    )
    columnas_a_mostrar = [
        "Fecha", "Hora", "Nombre_Sede", "Nombre_Completo_Cliente", "Telefono",
        "Nombre_Servicio", "Nombre_Completo_Barbero", "Precio"
    ]
    st.dataframe(
        df_citas_reales[columnas_a_mostrar].sort_values(by=["Fecha", "Hora"], ascending=[False, True]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "Precio": st.column_config.NumberColumn("Precio ($)", format="$ %.0f"),
            "Nombre_Completo_Cliente": "Cliente",
            "Nombre_Completo_Barbero": "Barbero",
            "Nombre_Sede": "Sede",
            "Nombre_Servicio": "Servicio",
            "Telefono": "Teléfono",
        }
    )