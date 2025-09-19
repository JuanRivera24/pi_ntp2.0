import streamlit as st
import pandas as pd
import data_manager as dm

st.title("🗓️ Gestión de Citas")

df_vista = dm.obtener_vista_citas_completa()
df_clientes, df_barberos, _, _ = dm.cargar_datos()

st.header("Filtro de Citas")

# Opciones para los filtros
opciones_barbero = ["Todos"] + list(df_barberos['Nombre_Barbero'].unique())
opciones_cliente = ["Todos"] + list(df_clientes['Nombre'].unique())

# Columnas para los filtros
col1, col2 = st.columns(2)
with col1:
    barbero_sel = st.selectbox("Filtrar por Barbero:", options=opciones_barbero)
with col2:
    cliente_sel = st.selectbox("Filtrar por Cliente:", options=opciones_cliente)

# Lógica de filtrado
df_filtrado = df_vista.copy()
if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Barbero'] == barbero_sel]
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre'] == cliente_sel]

st.header("Resultados")
st.dataframe(df_filtrado[[
    "Fecha", "Hora", "Nombre", "Telefono", "Nombre_Servicio", "Nombre_Barbero", "Precio"
]])