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

# --- INICIO CORRECCIÓN ---
# 1. Usar los nombres de columna correctos que definimos en data_manager.py
opciones_barbero = ["Todos"] + list(df_filtrado_por_sede['Nombre_Barbero'].unique())
opciones_cliente = ["Todos"] + list(df_filtrado_por_sede['Nombre_Cliente'].unique())
# --- FIN CORRECCIÓN ---

barbero_sel = st.sidebar.selectbox("Filtrar por Barbero:", options=opciones_barbero)
cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", options=opciones_cliente)

min_fecha = df_filtrado_por_sede['Fecha'].min() if not df_filtrado_por_sede.empty else datetime.now().date()
max_fecha = df_filtrado_por_sede['Fecha'].max() if not df_filtrado_por_sede.empty else datetime.now().date()

fecha_sel = st.sidebar.date_input(
    "Filtrar por Fecha:",
    value=(min_fecha, max_fecha),
    min_value=min_fecha,
    max_value=max_fecha
)

df_filtrado = df_filtrado_por_sede.copy()

# --- INICIO CORRECCIÓN ---
# 2. Usar los nombres correctos en la lógica de filtrado
if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Barbero'] == barbero_sel]
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Cliente'] == cliente_sel]
# --- FIN CORRECCIÓN ---

if len(fecha_sel) == 2:
    fecha_inicio, fecha_fin = fecha_sel
    df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_inicio) & (df_filtrado['Fecha'] <= fecha_fin)]

st.header(f"Resultados: {len(df_filtrado)} citas encontradas")

if df_filtrado.empty:
    st.info("No se encontraron citas que coincidan con los filtros seleccionados.")
else:
    total_ingresos_filtrado = df_filtrado['Precio'].sum()
    st.metric(
        label=f"💰 Ingresos para esta selección ({sede_sel})",
        value=f"${total_ingresos_filtrado:,.0f}"
    )

    # --- INICIO CORRECCIÓN ---
    # 3. Usar los nombres correctos al definir las columnas a mostrar
    columnas_a_mostrar = [
        "Fecha", "Hora", "Nombre_Sede", "Nombre_Cliente", "Telefono", 
        "Nombre_Servicio", "Nombre_Barbero", "Precio"
    ]
    
    st.dataframe(
        df_filtrado[columnas_a_mostrar].sort_values(by="Fecha", ascending=False),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "Precio": st.column_config.NumberColumn("Precio ($)", format="$ %.0f"),
            "Nombre_Cliente": st.column_config.TextColumn("Cliente"),
            "Nombre_Barbero": st.column_config.TextColumn("Barbero"),
            "Nombre_Sede": st.column_config.TextColumn("Sede"),
            "Nombre_Servicio": st.column_config.TextColumn("Servicio"),
        }
    )
    # --- FIN CORRECCIÓN ---