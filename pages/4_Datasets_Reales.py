import pandas as pd
import streamlit as st
import plotly.express as px
import re

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Peluquerías en Colombia",
    page_icon="✂️",
    layout="wide"
)

# --- 2. FUNCIÓN DE CARGA Y NORMALIZACIÓN ---
@st.cache_data
def load_and_normalize_dataset(url):
    """Carga y normaliza columnas de forma robusta."""
    try:
        df = pd.read_csv(url, low_memory=False)
        new_cols = []
        for col in df.columns:
            clean_col = str(col).lower().strip()
            clean_col = clean_col.replace('_', ' ').replace('-', ' ')
            clean_col = ' '.join(clean_col.split())
            replacements = {
                'razon social': 'nombre del establecimiento',
                'nombre establecimiento': 'nombre del establecimiento',
                'departamento domicilio': 'departamento',
                'municipio domicilio': 'municipio',
                'depto': 'departamento'
            }
            for old, new in replacements.items():
                if old in clean_col:
                    clean_col = new
            clean_col = re.sub(r'[^a-z0-9\s]+$', '', clean_col).strip()
            new_cols.append(clean_col)
        df.columns = new_cols
        return df
    except Exception as e:
        st.error(f"Error crítico al cargar o procesar los datos: {e}")
        try:
            df_partial = pd.read_csv(url, low_memory=False, nrows=5)
            st.warning(f"Columnas detectadas en el archivo: {df_partial.columns.tolist()}")
        except:
            pass
        return pd.DataFrame()

# ==============================================================================
# --- 3. DASHBOARDS ESPECÍFICOS (CON EL NACIONAL RECONSTRUIDO) ---
# ==============================================================================

def mostrar_dashboard_nacional(df):
    """
    Dashboard RECONSTRUIDO para el dataset Nacional.
    Ahora usa 'municipio comercial' ya que 'departamento' y 'ciudad' no existen.
    """
    st.sidebar.header("🔍 Filtros Nacionales")
    
    df_filtrado = df.copy()
    
    # --- Filtro por nombre ---
    st.sidebar.subheader("Filtrar por Establecimiento")
    if 'nombre del establecimiento' in df_filtrado.columns:
        nombres = ['Todos'] + sorted(df_filtrado['nombre del establecimiento'].dropna().unique())
        nombre_sel = st.sidebar.selectbox("Selecciona un nombre (puedes escribir para buscar)", nombres)
        if nombre_sel != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['nombre del establecimiento'] == nombre_sel]

    # --- Filtro por ubicación (usando la columna que sí existe) ---
    st.sidebar.subheader("Filtrar por Ubicación")
    if 'municipio comercial' in df_filtrado.columns:
        municipios = ['Todos'] + sorted(df_filtrado['municipio comercial'].dropna().unique())
        municipio_sel = st.sidebar.selectbox("Municipio Comercial", municipios)
        if municipio_sel != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['municipio comercial'] == municipio_sel]

    st.header("Métricas Clave a Nivel Nacional")
    total_registros = len(df_filtrado)
    total_municipios = df_filtrado['municipio comercial'].nunique() if 'municipio comercial' in df_filtrado.columns else 0
    municipio_comun = df_filtrado['municipio comercial'].mode()[0] if total_municipios > 0 and not df_filtrado['municipio comercial'].mode().empty else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("💈 Establecimientos Encontrados", f"{total_registros:,}")
    col2.metric("🗺️ Municipios en Selección", f"{total_municipios}")
    col3.metric("📍 Municipio Más Común", municipio_comun)
    
    st.header("Análisis Visual Nacional")
    if 'municipio comercial' in df_filtrado.columns:
        st.subheader("Establecimientos por Municipio Comercial")
        conteo_mun = df_filtrado['municipio comercial'].value_counts().nlargest(15).reset_index()
        fig = px.bar(conteo_mun, x='municipio comercial', y='count', text_auto=True, title="Top 15 Municipios")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No se encontró la columna 'municipio comercial' para generar gráficos.")
        
    return df_filtrado

def mostrar_dashboard_risaralda(df):
    """Dashboard para Risaralda con gráfico de barras."""
    st.sidebar.header("🔍 Filtros para Risaralda")
    df_filtrado = df.copy()
    municipios = ['Todos'] + sorted(df['municipio'].dropna().unique())
    mun_sel = st.sidebar.selectbox("Municipio de Risaralda", municipios)
    if mun_sel != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['municipio'] == mun_sel]
    st.header("Métricas Clave para Risaralda")
    total_registros = len(df_filtrado)
    municipio_comun = df_filtrado['municipio'].mode()[0] if not df_filtrado.empty else "N/A"
    col1, col2 = st.columns(2)
    col1.metric("💈 Establecimientos en Selección", f"{total_registros:,}")
    col2.metric("📍 Municipio Más Común", municipio_comun)
    st.header("Análisis Visual para Risaralda")
    st.subheader("Distribución de Establecimientos por Municipio")
    conteo_mun = df_filtrado['municipio'].value_counts().reset_index()
    fig = px.bar(conteo_mun, x='municipio', y='count', text_auto=True, title="Conteos por Municipio en Risaralda")
    fig.update_layout(xaxis_title="Municipio", yaxis_title="Cantidad de Establecimientos")
    st.plotly_chart(fig, use_container_width=True)
    return df_filtrado

def mostrar_dashboard_local(df):
    """Dashboard para el dataset de Estética Local."""
    st.sidebar.header("🔍 Filtros Locales")
    df_filtrado = df.copy()
    barrios = ['Todos'] + sorted(df['barrio'].dropna().unique())
    barrio_sel = st.sidebar.selectbox("Barrio", barrios)
    if barrio_sel != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['barrio'] == barrio_sel]
    st.header("Métricas Clave Locales")
    total_registros = len(df_filtrado)
    barrio_comun = df_filtrado['barrio'].mode()[0] if not df_filtrado.empty else "N/A"
    col1, col2 = st.columns(2)
    col1.metric("💈 Establecimientos Encontrados", f"{total_registros:,}")
    col2.metric("📍 Barrio Más Común", barrio_comun)
    st.header("Análisis Visual Local")
    st.subheader("Top 15 Barrios con más Establecimientos")
    conteo_barrio = df_filtrado['barrio'].value_counts().nlargest(15).reset_index()
    fig = px.bar(conteo_barrio, x='barrio', y='count', text_auto=True, title="Establecimientos por Barrio")
    st.plotly_chart(fig, use_container_width=True)
    return df_filtrado

# ==============================================================================
# --- 4. APLICACIÓN PRINCIPAL ---
# ==============================================================================
def app():
    st.title("📈 Dashboard de Peluquerías y Salones de Belleza en Colombia")
    st.markdown("---")
    datasets = {
        "Nacional - Establecimientos de Belleza": "https://www.datos.gov.co/api/views/e27n-di57/rows.csv?accessType=DOWNLOAD",
        "Risaralda - Estética Facial y Corporal": "https://www.datos.gov.co/api/views/92e4-cjqu/rows.csv?accessType=DOWNLOAD",
        "Estética Local (Ejemplo)": "https://www.datos.gov.co/api/views/mwxa-drpn/rows.csv?accessType=DOWNLOAD",
    }
    st.subheader("Paso 1: Selecciona un conjunto de datos para analizar")
    opcion_dataset = st.selectbox("Elige el dataset que quieres visualizar:", list(datasets.keys()))
    df_original = load_and_normalize_dataset(datasets[opcion_dataset])
    if df_original.empty:
        st.warning("No se pudieron cargar los datos.")
        st.stop()
    try:
        if opcion_dataset == "Nacional - Establecimientos de Belleza":
            df_final = mostrar_dashboard_nacional(df_original)
        elif opcion_dataset == "Risaralda - Estética Facial y Corporal":
            df_final = mostrar_dashboard_risaralda(df_original)
        elif opcion_dataset == "Estética Local (Ejemplo)":
            df_final = mostrar_dashboard_local(df_original)
        else:
            df_final = df_original
            st.info("Mostrando datos crudos.")
    except KeyError as e:
        st.error(f"Error de columna: No se pudo encontrar la columna esperada {e}.")
        st.info("La estructura del archivo de datos puede haber cambiado.")
        st.write("Columnas encontradas después de la normalización:")
        st.write(df_original.columns.tolist())
        df_final = df_original
    st.markdown("---")
    st.header("Explorador de Datos")
    st.write(f"Mostrando {len(df_final)} de {len(df_original)} registros según los filtros.")
    st.dataframe(df_final)

if __name__ == "__main__":
    app()