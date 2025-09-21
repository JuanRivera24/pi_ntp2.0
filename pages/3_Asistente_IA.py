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

# --- PESTAÑA 2: ANALISTA INTERACTIVO (VERSIÓN CON ANÁLISIS AVANZADO Y TEMPORAL) ---
with tab_analista:
    st.header("🕵️ Chatea con tus Datos")
    st.markdown("Hazme una pregunta directa sobre los datos filtrados y te ayudaré a encontrar la respuesta de forma objetiva.")
    
    st.info(f"Estoy listo para analizar las **{len(df_filtrado)} citas** que coinciden con tus filtros. ¡Pregúntame lo que necesites!")

    pregunta_usuario = st.text_input(
        "Escribe tu pregunta aquí:", 
        placeholder="Ej: ¿Qué mes tuvimos más ganancias?"
    )

    if st.button("🔍 Analizar y Responder"):
        if not model:
            st.error("No puedo conectarme con mi motor de IA en este momento.")
        elif not pregunta_usuario:
            st.warning("Por favor, escribe una pregunta para que pueda analizar los datos.")
        elif df_filtrado.empty:
            st.warning("No hay datos disponibles para los filtros que seleccionaste.")
        else:
            with st.spinner("Realizando un análisis profundo y consultando a la IA... 🧐"):
                
                # Aseguramos que la columna 'Fecha' sea del tipo datetime para los cálculos
                df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])

                # --- RESÚMENES DE PANDAS (INCLUYENDO EL NUEVO ANÁLISIS TEMPORAL) ---

                # 1. Métricas Generales
                total_citas = len(df_filtrado)
                total_ingresos = df_filtrado['Precio'].sum()

                # 2. Resumen por Servicio
                resumen_servicios = df_filtrado.groupby('Nombre_Servicio').agg(
                    Numero_de_Citas=('Precio', 'count'),
                    Ingresos_Totales=('Precio', 'sum')
                ).nlargest(5, 'Ingresos_Totales').to_string()

                # 3. Resumen por Barbero
                resumen_barberos = df_filtrado.groupby('Nombre_Completo_Barbero').agg(
                    Numero_de_Citas=('Precio', 'count'),
                    Ingresos_Totales=('Precio', 'sum')
                ).nlargest(5, 'Ingresos_Totales').to_string()

                # 4. Análisis del Cliente más Fiel
                # (Este código se mantiene igual que la versión anterior)
                cliente_mas_fiel_info = ""
                top_clientes = df_filtrado['Nombre_Completo_Cliente'].value_counts()
                if not top_clientes.empty:
                    # ... (el resto del código del cliente fiel va aquí, sin cambios)
                    nombre_cliente_fiel = top_clientes.index[0]
                    visitas_cliente_fiel = top_clientes.iloc[0]
                    df_cliente_fiel = df_filtrado[df_filtrado['Nombre_Completo_Cliente'] == nombre_cliente_fiel]
                    servicios_cliente_fiel = df_cliente_fiel['Nombre_Servicio'].value_counts().nlargest(3).to_string()
                    dias_entre_visitas = df_cliente_fiel['Fecha'].sort_values().diff().dt.days.mean()
                    cliente_mas_fiel_info = f"""
Análisis del Cliente Más Fiel ({nombre_cliente_fiel}):
- Visitas Totales: {visitas_cliente_fiel}
- Frecuencia Promedio: Cada {dias_entre_visitas:.1f} días.
- Sus 3 servicios favoritos:
{servicios_cliente_fiel}"""

                # --- ¡NUEVO! 5. ANÁLISIS TEMPORAL (POR MES Y DÍA DE LA SEMANA) ---
                analisis_temporal = ""
                # Solo realizamos el análisis si hay más de un día de datos
                if df_filtrado['Fecha'].nunique() > 1:
                    # Extraemos el nombre del mes y el día de la semana
                    df_filtrado['Mes'] = df_filtrado['Fecha'].dt.strftime('%Y-%m (%B)') # Formato: 2023-10 (Octubre)
                    df_filtrado['Dia_Semana'] = df_filtrado['Fecha'].dt.day_name()

                    # Calculamos ingresos por mes
                    ingresos_por_mes = df_filtrado.groupby('Mes')['Precio'].sum().sort_values(ascending=False).to_string()
                    
                    # Calculamos citas por día de la semana
                    citas_por_dia = df_filtrado['Dia_Semana'].value_counts().to_string()

                    analisis_temporal = f"""
Análisis Temporal:
- Ingresos por Mes:
{ingresos_por_mes}

- Citas por Día de la Semana:
{citas_por_dia}
"""

                # Unimos todos los resúmenes en un solo contexto para la IA
                contexto_resumido = f"""
Resumen General:
- Citas Totales: {total_citas}
- Ingresos Totales: ${total_ingresos:,.2f}

{analisis_temporal}

Resumen por Servicio (Top 5 por Ingresos):
{resumen_servicios}

Resumen por Barbero (Top 5 por Ingresos):
{resumen_barberos}
                
{cliente_mas_fiel_info}
                """

                # El prompt se mantiene igual, ya que es robusto. Lo importante es el contexto.
                prompt_analista_final = f"""
                Eres "Alex", un asistente de análisis de datos amigable, inteligente y muy preciso. Tu trabajo es responder preguntas sobre el negocio de una barbería.

                **REGLAS CLAVE:**
                1.  **Usa solo los datos del resumen:** Tu única fuente de información es el resumen que te proporciono. No inventes datos.
                2.  **Sé directo y claro:** Responde a la pregunta del usuario de forma natural y conversacional. Evita saludos formales. Ve directo al grano.
                3.  **Si no sabes, dilo:** Si la información no está en el resumen para responder, explícalo amablemente.

                **RESUMEN DE DATOS PARA TU ANÁLISIS:**
                ---
                {contexto_resumido}
                ---

                **PREGUNTA DEL USUARIO:**
                "{pregunta_usuario}"

                **Instrucciones:**
                Analiza el resumen y responde la pregunta de forma concisa y basada en la evidencia.
                """
                
                try:
                    respuesta_ia = model.generate_content(prompt_analista_final)
                    st.markdown("### 💡 Aquí está tu análisis:")
                    st.success(respuesta_ia.text)

                except Exception as e:
                    st.error(f"¡Oops! Algo salió mal al intentar procesar tu pregunta. Detalle del error: {e}")
                    
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