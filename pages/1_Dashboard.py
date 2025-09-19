import streamlit as st
import data_manager as dm # Importamos nuestro módulo de datos

st.title("📊 Dashboard General")

# Obtenemos la vista completa de citas desde nuestro manager
df_vista = dm.obtener_vista_citas_completa()

st.header("Métricas Clave")

total_ingresos = df_vista['Precio'].sum()
total_citas = len(df_vista)
# Usamos .get(0, 'N/A') para evitar errores si no hay datos
servicio_popular = df_vista['Nombre_Servicio'].mode().get(0, "N/A")

col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales (Histórico)", f"${total_ingresos:,.0f}")
col2.metric("Total Citas Registradas", total_citas)
col3.metric("Servicio Más Popular", servicio_popular)

st.header("Ingresos por Servicio")
ingresos_servicio = df_vista.groupby('Nombre_Servicio')['Precio'].sum()
st.bar_chart(ingresos_servicio)

st.header("Productos desde API (Mockoon)")
df_productos = dm.cargar_productos_api()
if not df_productos.empty:
    st.table(df_productos)
else:
    st.warning("No se pudieron cargar los datos de productos desde la API.")