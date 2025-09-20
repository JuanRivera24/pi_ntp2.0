import streamlit as st
import pandas as pd
import data_manager as dm
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="Gestión de Citas | Kingdom Barber", page_icon="🗓️", layout="wide")

st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🗓️ Gestión de Citas</h1>", unsafe_allow_html=True)
st.markdown("### Filtra, busca y gestiona todas las citas de la barbería.")
st.markdown("---")

@st.cache_data
def cargar_datos_citas():
    df_vista = dm.obtener_vista_citas_completa() 
    _, _, _, _, df_sedes = dm.cargar_datos()
    # Convertimos a fecha, los valores NaN se convertirán a NaT (Not a Time)
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha']).dt.date
    return df_vista, df_sedes

df_vista, df_sedes = cargar_datos_citas()

st.sidebar.header("🔍 Filtros Avanzados")

lista_sedes = ['Todas'] + df_sedes['Nombre_Sede'].unique().tolist()
sede_sel = st.sidebar.selectbox("Filtrar por Sede:", options=lista_sedes)

if sede_sel != "Todas":
    df_filtrado_por_sede = df_vista[df_vista['Nombre_Sede'] == sede_sel]
else:
    df_filtrado_por_sede = df_vista.copy()

# Usamos las columnas de NOMBRE COMPLETO para las opciones de los filtros.
# Usamos sorted() para que las listas aparezcan en orden alfabético.
opciones_barbero = ["Todos"] + sorted(list(df_filtrado_por_sede['Nombre_Completo_Barbero'].dropna().unique()))
opciones_cliente = ["Todos"] + sorted(list(df_filtrado_por_sede['Nombre_Completo_Cliente'].dropna().unique()))

barbero_sel = st.sidebar.selectbox("Filtrar por Barbero:", options=opciones_barbero)
cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", options=opciones_cliente)

# --- INICIO DE LA CORRECCIÓN ---
# Filtramos los valores nulos (NaT) de la columna Fecha ANTES de calcular min() y max()
fechas_validas = df_filtrado_por_sede['Fecha'].dropna()

min_fecha = fechas_validas.min() if not fechas_validas.empty else datetime.now().date()
max_fecha = fechas_validas.max() if not fechas_validas.empty else datetime.now().date()

fecha_sel = st.sidebar.date_input(
    "Filtrar por Rango de Fecha:",
    value=(min_fecha, max_fecha),
    min_value=min_fecha,
    max_value=max_fecha,
    # Añadimos un key para evitar problemas de refresco en Streamlit
    key="date_range_picker" 
)
# --- FIN DE LA CORRECCIÓN ---


df_filtrado = df_filtrado_por_sede.copy()

# Usamos las columnas de NOMBRE COMPLETO en la lógica de filtrado.
if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Barbero'] == barbero_sel]
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Cliente'] == cliente_sel]

if len(fecha_sel) == 2:
    fecha_inicio, fecha_fin = fecha_sel
    # Nos aseguramos de filtrar solo las filas que tienen una fecha válida
    df_filtrado = df_filtrado.dropna(subset=['Fecha'])
    df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_inicio) & (df_filtrado['Fecha'] <= fecha_fin)]

st.header(f"Resultados: {len(df_filtrado[df_filtrado['ID_Cita'].notna()])} citas encontradas")

if df_filtrado.empty or df_filtrado['ID_Cita'].isnull().all():
    st.info("No se encontraron citas que coincidan con los filtros seleccionados.")
else:
    # Calculamos ingresos solo sobre las filas que tienen citas reales
    total_ingresos_filtrado = df_filtrado['Precio'].sum()
    st.metric(
        label=f"💰 Ingresos para esta selección ({sede_sel})",
        value=f"${total_ingresos_filtrado:,.0f}"
    )

    columnas_a_mostrar = [
        "Fecha", "Hora", "Nombre_Sede", "Nombre_Completo_Cliente", "Telefono", 
        "Nombre_Servicio", "Nombre_Completo_Barbero", "Precio"
    ]
    
    # Mostramos solo las filas que corresponden a citas reales
    st.dataframe(
        df_filtrado.dropna(subset=['ID_Cita'])[columnas_a_mostrar].sort_values(by="Fecha", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "Precio": st.column_config.NumberColumn("Precio ($)", format="$ %.0f"),
            "Nombre_Completo_Cliente": st.column_config.TextColumn("Cliente"),
            "Nombre_Completo_Barbero": st.column_config.TextColumn("Barbero"),
            "Nombre_Sede": st.column_config.TextColumn("Sede"),
            "Nombre_Servicio": st.column_config.TextColumn("Servicio"),
            "Telefono": st.column_config.TextColumn("Teléfono"),
        }
    )