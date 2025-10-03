import streamlit as st
import pandas as pd
import data_manager as dm
from datetime import datetime

st.set_page_config(page_title="Gestión de Citas | Kingdom Barber", page_icon="🗓️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🗓️ Gestión de Citas</h1>", unsafe_allow_html=True)
st.markdown("### Filtra, busca y gestiona todas las citas de la barbería.")
st.markdown("---")

# --- CORRECCIÓN ---
# La función ahora devuelve dos DataFrames, los "desempaquetamos" en dos variables.
df_vista, df_sedes = dm.obtener_vista_citas_completa()

if df_vista.empty:
    st.error("No se pudieron cargar los datos de citas desde la API. Asegúrate de que la API de Java esté corriendo.")
    st.stop()

# --- El resto del código funciona con las variables correctas ---
st.sidebar.header("🔍 Filtros Avanzados")

lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_sel = st.sidebar.selectbox("Filtrar por Sede:", options=lista_sedes)

if sede_sel != "Todas":
    df_filtrado_por_sede = df_vista[df_vista['Nombre_Sede'] == sede_sel]
else:
    df_filtrado_por_sede = df_vista.copy()

opciones_barbero = ["Todos"] + sorted(list(df_filtrado_por_sede['Nombre_Completo_Barbero'].dropna().unique()))
opciones_cliente = ["Todos"] + sorted(list(df_filtrado_por_sede['Nombre_Completo_Cliente'].dropna().unique()))

barbero_sel = st.sidebar.selectbox("Filtrar por Barbero:", options=opciones_barbero)
cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", options=opciones_cliente)

fechas_validas = df_filtrado_por_sede['Fecha'].dropna()
min_fecha = fechas_validas.min().date() if not fechas_validas.empty else datetime.now().date()
max_fecha = fechas_validas.max().date() if not fechas_validas.empty else datetime.now().date()

fecha_sel = st.sidebar.date_input(
    "Filtrar por Rango de Fecha:",
    value=(min_fecha, max_fecha),
    min_value=min_fecha,
    max_value=max_fecha,
    key="date_range_picker_gestion"
)

df_filtrado = df_filtrado_por_sede.copy()

if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Barbero'] == barbero_sel]
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Cliente'] == cliente_sel]
if len(fecha_sel) == 2:
    fecha_inicio, fecha_fin = fecha_sel
    df_filtrado = df_filtrado.dropna(subset=['Fecha'])
    df_filtrado = df_filtrado[(df_filtrado['Fecha'].dt.date >= fecha_inicio) & (df_filtrado['Fecha'].dt.date <= fecha_fin)]

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
        df_citas_reales[columnas_a_mostrar].sort_values(by="Fecha", ascending=False),
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