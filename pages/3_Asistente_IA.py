import streamlit as st
import pandas as pd
from data_manager import obtener_vista_citas_completa
from report_generator import generar_pdf_reporte
import google.generativeai as genai # Importamos la librería de Google
import traceback # Para un mejor manejo de errores

# --- Configuración de la Página ---
st.set_page_config(
    page_title="Asistente IA",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Asistente de Inteligencia Artificial")
st.markdown("Tu centro de mando para análisis avanzados, reportes y marketing inteligente.")

# --- Cargar y cachear los datos ---
@st.cache_data
def cargar_datos():
    return obtener_vista_citas_completa()

df_citas_completa = cargar_datos()

# --- Función para generar análisis con Gemini ---
def generar_analisis_ia_con_gemini(datos_filtrados_str):
    """
    Utiliza el API de Gemini para generar un análisis de negocio a partir de los datos.
    """
    try:
        # Configurar el API key desde los secrets de Streamlit
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)

        # Crear el modelo
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        prompt = f"""
        Eres un analista de negocios experto para una cadena de barberías.
        Analiza los siguientes datos de citas, que están en formato de texto:
        {datos_filtrados_str}

        Basado en estos datos, proporciona un análisis conciso pero profundo que incluya:
        1.  **Resumen Ejecutivo:** Un párrafo corto con los hallazgos más importantes.
        2.  **Observaciones Clave:** 3 a 5 puntos (bullet points) destacando tendencias, patrones o anomalías (ej. qué barbero es más popular, qué servicio genera más ingresos, qué día es el más concurrido).
        3.  **Recomendaciones Estratégicas:** 2 o 3 acciones concretas que el negocio podría tomar para mejorar, basadas en los datos (ej. ofrecer una promoción en un día de baja afluencia, capacitar a un barbero en un servicio popular, etc.).

        El tono debe ser profesional, directo y orientado a la acción.
        """
        
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        st.error(f"Error al conectar con el API de Gemini: {e}")
        st.error("Por favor, asegúrate de que tu clave de API está configurada correctamente en los secrets de Streamlit.")
        # Imprime el traceback completo en la consola para depuración
        print("Traceback completo del error de Gemini:")
        traceback.print_exc()
        return "No se pudo generar el análisis debido a un error de conexión con la IA."


# --- Barra Lateral de Filtros ---
with st.sidebar:
    st.header("Filtros para el Reporte")
    
    # Filtro de Sede
    sedes_disponibles = ["Todas"] + df_citas_completa['Nombre_Sede'].unique().tolist()
    sede_seleccionada = st.selectbox("Selecciona una Sede", sedes_disponibles)

    # Filtro de Fechas
    min_date = df_citas_completa['Fecha'].min()
    max_date = df_citas_completa['Fecha'].max()
    rango_fechas = st.date_input(
        "Selecciona un Rango de Fechas",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Filtro de Barbero
    barberos_disponibles = ["Todos"] + df_citas_completa['Nombre_Completo_Barbero'].dropna().unique().tolist()
    barbero_seleccionado = st.selectbox("Selecciona un Barbero", barberos_disponibles)

    # Filtro de Servicio
    servicios_disponibles = ["Todos"] + df_citas_completa['Nombre_Servicio'].dropna().unique().tolist()
    servicio_seleccionado = st.selectbox("Selecciona un Servicio", servicios_disponibles)

# --- Aplicar filtros a los datos ---
df_filtrado = df_citas_completa.copy()

if sede_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Sede'] == sede_seleccionada]

if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
    df_filtrado = df_filtrado[(df_filtrado['Fecha'] >= pd.to_datetime(fecha_inicio)) & (df_filtrado['Fecha'] <= pd.to_datetime(fecha_fin))]

if barbero_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Barbero'] == barbero_seleccionado]

if servicio_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Nombre_Servicio'] == servicio_seleccionado]

# --- Interfaz Principal con Pestañas ---
tab_reportes, tab_analista, tab_marketing = st.tabs([
    "📈 Generador de Reportes", 
    "🕵️ Analista de Datos Interactivo (Próximamente)", 
    "🎯 Asistente de Marketing (Próximamente)"
])

with tab_reportes:
    st.header("Generador de Reportes a Medida")
    st.markdown("Selecciona los filtros en la barra lateral y haz clic en el botón para generar un reporte en PDF con análisis de IA.")

    if st.button("🚀 Generar Reporte PDF"):
        if df_filtrado.empty:
            st.warning("No hay datos disponibles para los filtros seleccionados. Por favor, ajusta tu selección.")
        else:
            with st.spinner("Preparando datos y consultando a la IA... 🤖"):
                # Convertir una muestra del dataframe a string para enviarlo a la IA
                # Se usa una muestra para no exceder los límites de tokens del prompt
                muestra_datos_str = df_filtrado.head(50).to_string()
                
                # Generar el análisis con Gemini
                analisis_ia = generar_analisis_ia_con_gemini(muestra_datos_str)
            
            with st.spinner("Creando el archivo PDF... 📄"):
                # Preparar el contexto para el reporte
                contexto_reporte = {
                    "sede": sede_seleccionada,
                    "rango_fechas": f"{rango_fechas[0].strftime('%d/%m/%Y')} - {rango_fechas[1].strftime('%d/%m/%Y')}",
                    "barbero": barbero_seleccionado,
                    "servicio": servicio_seleccionado,
                }
                
                # Generar el PDF
                pdf_bytes = generar_pdf_reporte(df_filtrado, analisis_ia, contexto_reporte)
            
            st.success("¡Reporte generado con éxito!")
            
            # Crear el nombre del archivo dinámicamente
            nombre_archivo = f"Reporte_{sede_seleccionada.replace(' ', '_')}_{rango_fechas[0].strftime('%Y%m%d')}_{rango_fechas[1].strftime('%Y%m%d')}.pdf"

            st.download_button(
                label="📥 Descargar Reporte PDF",
                data=pdf_bytes,
                file_name=nombre_archivo,
                mime="application/pdf"
            )

with tab_analista:
    st.header("Chatea con tus Datos")
    st.info("Funcionalidad en desarrollo. Próximamente podrás hacer preguntas en lenguaje natural sobre tu negocio y obtener respuestas al instante.")

with tab_marketing:
    st.header("Crea Campañas de Marketing Inteligentes")
    st.info("Funcionalidad en desarrollo. En el futuro, la IA te ayudará a identificar clientes para campañas específicas y a generar borradores de correos o mensajes.")
