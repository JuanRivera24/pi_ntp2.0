import streamlit as st
import pandas as pd
import data_manager as dm
from datetime import datetime
import sys
import os

# Añade la carpeta raíz del proyecto a la ruta de búsqueda de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# --- Configuración de la Página ---
st.set_page_config(page_title="Gestión de Citas | Kingdom Barber", page_icon="🗓️", layout="wide")

# --- Título Principal ---
st.markdown("<h1 style='text-align: center; color: #D4AF37;'>🗓️ Gestión de Citas</h1>", unsafe_allow_html=True)
st.markdown("### Filtra, busca y gestiona todas las citas de la barbería.")
st.markdown("---")

# --- Carga de Datos (usando cache para eficiencia) ---
@st.cache_data
def cargar_datos_citas():
    df_vista = dm.obtener_vista_citas_completa()
    # Asegurarnos de que la columna 'Fecha' sea del tipo datetime
    df_vista['Fecha'] = pd.to_datetime(df_vista['Fecha']).dt.date
    return df_vista

df_vista = cargar_datos_citas()

# --- Panel de Filtros Avanzados ---
st.sidebar.header("🔍 Filtros Avanzados")

# Opciones para los filtros (incluyendo "Todos")
opciones_barbero = ["Todos"] + list(df_vista['Nombre_Barbero'].unique())
# --- CORRECCIÓN 1 ---
opciones_cliente = ["Todos"] + list(df_vista['Nombre'].unique()) # Se cambió 'Nombre_Cliente' por 'Nombre'

# Crear filtros en la barra lateral para un layout más limpio
barbero_sel = st.sidebar.selectbox("Filtrar por Barbero:", options=opciones_barbero)
cliente_sel = st.sidebar.selectbox("Filtrar por Cliente:", options=opciones_cliente)

# Nuevo filtro por rango de fechas
fecha_sel = st.sidebar.date_input(
    "Filtrar por Fecha:",
    value=(df_vista['Fecha'].min(), df_vista['Fecha'].max()), # Rango por defecto: desde la primera hasta la última cita
    min_value=df_vista['Fecha'].min(),
    max_value=df_vista['Fecha'].max()
)

# Lógica de filtrado
df_filtrado = df_vista.copy()

if barbero_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Barbero'] == barbero_sel]
# --- CORRECCIÓN 2 ---
if cliente_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre'] == cliente_sel] # Se cambió 'Nombre_Cliente' por 'Nombre'

if len(fecha_sel) == 2: # El date_input devuelve una tupla de dos fechas
    fecha_inicio, fecha_fin = fecha_sel
    df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= fecha_inicio) & (df_filtrado['Fecha'] <= fecha_fin)]


# --- Visualización de Resultados ---
st.header(f"Resultados: {len(df_filtrado)} citas encontradas")

if df_filtrado.empty:
    st.info("No se encontraron citas que coincidan con los filtros seleccionados.")
else:
    # Mostramos métricas rápidas sobre los datos filtrados
    total_ingresos_filtrado = df_filtrado['Precio'].sum()
    st.metric(
        label="💰 Ingresos para esta selección",
        value=f"${total_ingresos_filtrado:,.0f}"
    )

    # Columnas que queremos mostrar y en qué orden
    # --- CORRECCIÓN 3 ---
    columnas_a_mostrar = [
        "Fecha", "Hora", "Nombre", "Telefono", "Nombre_Servicio", "Nombre_Barbero", "Precio" # Se cambió 'Nombre_Cliente' por 'Nombre'
    ]
    
    # Usamos st.dataframe para una tabla interactiva y con mejor formato
    st.dataframe(
        df_filtrado[columnas_a_mostrar].sort_values(by="Fecha", ascending=False), # Ordenamos por fecha más reciente
        use_container_width=True,
        hide_index=True, # Ocultamos el índice numérico que añade pandas
        column_config={ # Mejoramos la visualización de las columnas
            "Fecha": st.column_config.DateColumn(
                "Fecha",
                format="DD/MM/YYYY",
            ),
            "Precio": st.column_config.NumberColumn(
                "Precio ($)",
                format="$ %.2f"
            ),
            # Añadimos un alias para la columna 'Nombre' para que se vea mejor en la tabla
            "Nombre": st.column_config.TextColumn(
                "Nombre del Cliente"
            )
        }
    )