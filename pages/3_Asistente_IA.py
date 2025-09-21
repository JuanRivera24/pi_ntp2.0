import streamlit as st
import pandas as pd
from data_manager import obtener_vista_citas_completa
from report_generator import generar_pdf_reporte
import google.generativeai as genai
import traceback

# --- Configuración de la Página (sin cambios) ---
st.set_page_config(page_title="Asistente IA", page_icon="🤖", layout="wide")
st.title("🤖 Asistente de Inteligencia Artificial")
st.markdown("Tu centro de mando para análisis avanzados, reportes y marketing inteligente.")

# --- Cargar y cachear los datos (sin cambios) ---
@st.cache_data
def cargar_datos():
    return obtener_vista_citas_completa()

df_citas_completa = cargar_datos()

# --- Conexión al API de Gemini (centralizada para reutilizar) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"No se pudo configurar la conexión con Google Gemini. Verifica tu API Key. Error: {e}")
    model = None

# --- Función para generar análisis de reportes (tu función original, sin cambios) ---
def generar_analisis_ia_con_gemini(datos_filtrados_str):
    if not model: return "El modelo de IA no está disponible."
    try:
        prompt = f"""
        Eres un analista de negocios experto para una cadena de barberías. Analiza los siguientes datos de citas:
        {datos_filtrados_str}
        Proporciona un análisis con:
        1. **Resumen Ejecutivo:** Párrafo corto con hallazgos importantes.
        2. **Observaciones Clave:** 3 a 5 puntos destacando tendencias.
        3. **Recomendaciones Estratégicas:** 2 o 3 acciones concretas.
        El tono debe ser profesional y orientado a la acción.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        traceback.print_exc()
        return "No se pudo generar el análisis debido a un error de conexión con la IA."

# --- Barra Lateral de Filtros (sin cambios) ---
with st.sidebar:
    st.header("Filtros para el Reporte")
    sedes_disponibles = ["Todas"] + df_citas_completa['Nombre_Sede'].unique().tolist()
    sede_seleccionada = st.selectbox("Selecciona una Sede", sedes_disponibles)
    min_date = df_citas_completa['Fecha'].min(); max_date = df_citas_completa['Fecha'].max()
    rango_fechas = st.date_input("Selecciona un Rango de Fechas", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    barberos_disponibles = ["Todos"] + df_citas_completa['Nombre_Completo_Barbero'].dropna().unique().tolist()
    barbero_seleccionado = st.selectbox("Selecciona un Barbero", barberos_disponibles)
    servicios_disponibles = ["Todos"] + df_citas_completa['Nombre_Servicio'].dropna().unique().tolist()
    servicio_seleccionado = st.selectbox("Selecciona un Servicio", servicios_disponibles)

# --- Aplicar filtros a los datos (sin cambios) ---
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

# --- Interfaz Principal con Pestañas (AHORA CON FUNCIONALIDAD) ---
tab_reportes, tab_analista, tab_marketing = st.tabs([
    "📈 Generador de Reportes", 
    "🕵️ Analista de Datos Interactivo", 
    "🎯 Asistente de Marketing"
])

# --- PESTAÑA 1: REPORTES (sin cambios, tu código original) ---
with tab_reportes:
    st.header("Generador de Reportes a Medida")
    st.markdown("Selecciona los filtros en la barra lateral y haz clic en el botón para generar un reporte en PDF con análisis de IA.")
    if st.button("🚀 Generar Reporte PDF"):
        if df_filtrado.empty:
            st.warning("No hay datos para los filtros seleccionados.")
        else:
            with st.spinner("Preparando datos y consultando a la IA... 🤖"):
                muestra_datos_str = df_filtrado.head(50).to_string()
                analisis_ia = generar_analisis_ia_con_gemini(muestra_datos_str)
            with st.spinner("Creando el archivo PDF... 📄"):
                contexto_reporte = {
                    "sede": sede_seleccionada,
                    "rango_fechas": f"{rango_fechas[0].strftime('%d/%m/%Y')} - {rango_fechas[1].strftime('%d/%m/%Y')}",
                    "barbero": barbero_seleccionado, "servicio": servicio_seleccionado,
                }
                pdf_bytes = generar_pdf_reporte(df_filtrado, analisis_ia, contexto_reporte)
            st.success("¡Reporte generado con éxito!")
            nombre_archivo = f"Reporte_{sede_seleccionada.replace(' ', '_')}_{rango_fechas[0].strftime('%Y%m%d')}_{rango_fechas[1].strftime('%Y%m%d')}.pdf"
            st.download_button(label="📥 Descargar Reporte PDF", data=pdf_bytes, file_name=nombre_archivo, mime="application/pdf")

# --- PESTAÑA 2: ANALISTA INTERACTIVO (VERSIÓN MEJORADA CON PERSONALIDAD) ---
with tab_analista:
    st.header("🕵️ Chatea con tus Datos")
    st.markdown("Hazme una pregunta sobre tus datos y te ayudaré a encontrar la respuesta. ¡Estoy aquí para asistirte!")
    
    # Muestra un resumen más amigable del contexto actual
    st.info(f"Estoy analizando **{len(df_filtrado)} citas** de la sede **{sede_seleccionada}**. ¡Pregúntame lo que necesites saber sobre este periodo!")

    pregunta_usuario = st.text_input(
        "Escribe tu pregunta aquí:", 
        placeholder="Ej: ¿Qué día de la semana tuvimos más clientes?"
    )

    if st.button("🔍 Preguntar al Asistente"):
        if not model:
            st.error("Lo siento, parece que no puedo conectarme con mi cerebro de IA en este momento.")
        elif not pregunta_usuario:
            st.warning("¡No seas tímido! Escríbeme una pregunta para que pueda ayudarte.")
        elif df_filtrado.empty:
            st.warning("Uhm... parece que no hay datos para analizar con los filtros que seleccionaste. ¿Probamos con otro rango de fechas?")
        else:
            with st.spinner("Consultando los registros y analizando los números... 🤔"):
                # Usamos una muestra representativa pero no abrumadora
                datos_contexto = df_filtrado.sample(min(len(df_filtrado), 100)).to_csv()

                # --- EL NUEVO PROMPT CON PERSONALIDAD ---
                prompt_analista_mejorado = f"""
                Adopta la personalidad de un asistente de análisis de datos amigable, inteligente y proactivo para el gerente de una barbería. Tu nombre es "Alex".
                
                Tu tarea es responder a la pregunta del gerente basándote únicamente en el siguiente extracto de datos en formato CSV.
                
                Datos para tu análisis:
                ---
                {datos_contexto}
                ---

                Pregunta del gerente: "{pregunta_usuario}"

                Debes estructurar tu respuesta de la siguiente manera, usando un tono conversacional y servicial:

                **Respuesta Directa:** 
                (Ofrece una respuesta clara y directa a la pregunta).

                **El Porqué:** 
                (Explica brevemente cómo llegaste a esa conclusión, mencionando los datos que usaste. Por ejemplo: "Llegué a esta conclusión al observar que...").

                **Dato Interesante:** 
                (Añade un pequeño insight o dato curioso que hayas notado en los datos y que esté relacionado con la pregunta. Si no encuentras nada, puedes omitir esta parte).

                Si los datos no son suficientes para responder, explícalo amablemente y sugiere qué tipo de datos necesitarías. No inventes información.
                """
                
                try:
                    respuesta_ia = model.generate_content(prompt_analista_mejorado)
                    # Usamos st.expander para una presentación más limpia y organizada
                    with st.expander("Aquí tienes tu análisis:", expanded=True):
                        st.markdown(respuesta_ia.text)
                except Exception as e:
                    st.error(f"¡Vaya! Tuve un problema al procesar tu pregunta. Aquí está el detalle técnico: {e}")

# --- PESTAÑA 3: ASISTENTE DE MARKETING (NUEVA FUNCIONALIDAD) ---
with tab_marketing:
    st.header("🎯 Asistente de Marketing Inteligente")
    st.markdown("Genera ideas y borradores para tus campañas de marketing basados en los datos.")

    col1, col2 = st.columns(2)
    with col1:
        tipo_campaña = st.selectbox(
            "Selecciona el objetivo de la campaña:",
            ["Atraer nuevos clientes", "Fidelizar clientes existentes", "Promocionar un servicio poco popular", "Aumentar citas en días flojos"]
        )
    with col2:
        canal_comunicacion = st.radio(
            "Selecciona el canal:",
            ("WhatsApp", "Email", "Redes Sociales"),
            horizontal=True
        )

    if st.button("💡 Generar Idea de Campaña"):
        if not model:
            st.error("El modelo de IA no está disponible.")
        elif df_filtrado.empty:
            st.warning("No hay suficientes datos para generar una idea de campaña con los filtros actuales.")
        else:
            with st.spinner("Creando una campaña brillante... ✨"):
                # Calculamos algunos insights rápidos con pandas para darle más contexto a la IA
                try:
                    servicio_menos_popular = df_filtrado['Nombre_Servicio'].value_counts().idxmin()
                    dia_mas_flojo = df_filtrado['Fecha'].dt.day_name().value_counts().idxmin()
                except Exception:
                    servicio_menos_popular = "n/a"
                    dia_mas_flojo = "n/a"

                prompt_marketing = f"""
                Eres un experto en marketing para barberías. Tu tarea es generar un borrador para una campaña de marketing.
                
                Contexto del negocio:
                - El objetivo de la campaña es: {tipo_campaña}
                - El canal de comunicación será: {canal_comunicacion}
                - Un servicio con pocas citas es: {servicio_menos_popular}
                - Un día con poca afluencia es: {dia_mas_flojo}

                Por favor, genera un borrador completo que incluya:
                1. **Nombre de la Campaña:** Un título pegadizo.
                2. **Público Objetivo:** ¿A quién se dirige?
                3. **Mensaje Principal:** El texto exacto para el {canal_comunicacion}. Debe ser persuasivo y claro.
                4. **Sugerencia Adicional:** Una idea extra para que la campaña sea más efectiva.

                Formatea tu respuesta usando Markdown (títulos con ##, negritas con **).
                """

                try:
                    respuesta_ia = model.generate_content(prompt_marketing)
                    st.markdown(respuesta_ia.text)
                except Exception as e:
                    st.error(f"Ocurrió un error al generar la campaña: {e}")