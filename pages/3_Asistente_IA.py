import streamlit as st
import pandas as pd
import data_manager as dm
from report_generator import generar_pdf_reporte
import google.generativeai as genai
import traceback
from io import StringIO
import sys
from PIL import Image
from datetime import datetime
from babel.dates import format_date # 1. IMPORTAMOS BABEL
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- 1. CONFIGURACIÓN DE PÁGINA Y CONEXIÓN A LA IA ---
st.set_page_config(page_title="Asistente IA", page_icon="🤖", layout="wide")
st.title("🤖 Asistente de Inteligencia Artificial")
st.markdown("Tu centro de mando para análisis avanzados, reportes y marketing inteligente.")

model = None
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    # Se mantiene tu modelo de IA especificado
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20') # Modelo actualizado a uno estándar
except Exception as e:
    st.error(f"No se pudo configurar la conexión con Google Gemini. Verifica tu API Key. Error: {e}")

# --- 2. CARGA DE DATOS CENTRALIZADA DESDE LA API ---
@st.cache_data
def cargar_datos_completos():
    """Llama al data_manager una sola vez para obtener todos los datos."""
    return dm.obtener_vista_citas_completa()

df_vista_completa, df_sedes = cargar_datos_completos()

if df_vista_completa.empty:
    st.error("No se pudieron cargar los datos desde la API. Asegúrate de que la API de Java esté corriendo.")
    st.stop()

# --- 3. FILTROS GLOBALES EN LA BARRA LATERAL ---
with st.sidebar:
    st.header("Filtros Globales")
    
    lista_sedes_ia = ['Todas'] + df_sedes['Nombre_Sede'].dropna().unique().tolist()
    sede_seleccionada = st.selectbox("Selecciona una Sede", lista_sedes_ia, key="sede_ia")
    
    fechas_validas = df_vista_completa['Fecha'].dropna()
    min_date = fechas_validas.min().date() if not fechas_validas.empty else datetime.now().date()
    max_date = fechas_validas.max().date() if not fechas_validas.empty else datetime.now().date()
    if min_date > max_date: min_date = max_date
    rango_fechas = st.date_input("Selecciona un Rango de Fechas", value=(min_date, max_date), min_value=min_date, max_value=max_date, key="date_ia")
    
    lista_barberos_ia = ['Todos'] + sorted(df_vista_completa['Nombre_Completo_Barbero'].dropna().unique().tolist())
    barbero_seleccionado = st.selectbox("Selecciona un Barbero", lista_barberos_ia, key="barbero_ia")
    
    lista_servicios_ia = ['Todos'] + sorted(df_vista_completa['Nombre_Servicio'].dropna().unique().tolist())
    servicio_seleccionado = st.selectbox("Selecciona un Servicio", lista_servicios_ia, key="servicio_ia")

# --- 4. APLICACIÓN DE FILTROS ---
df_filtrado = df_vista_completa.copy()
if sede_seleccionada != "Todas": df_filtrado = df_filtrado[df_filtrado['Nombre_Sede'] == sede_seleccionada]

if len(rango_fechas) == 2:
    fecha_inicio, fecha_fin = rango_fechas
    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'], errors='coerce')
    df_filtrado.dropna(subset=['Fecha'], inplace=True)
    df_filtrado = df_filtrado[
        (df_filtrado['Fecha'].dt.date >= fecha_inicio) & 
        (df_filtrado['Fecha'].dt.date <= fecha_fin)
    ]

if barbero_seleccionado != "Todos": df_filtrado = df_filtrado[df_filtrado['Nombre_Completo_Barbero'] == barbero_seleccionado]
if servicio_seleccionado != "Todos": df_filtrado = df_filtrado[df_filtrado['Nombre_Servicio'] == servicio_seleccionado]

lista_cortes_populares = [
    # --- Cortes Cortos ---
    "Buzz Cut", "Crew Cut", "High and Tight", "Ivy League", "French Crop",
    "Pixie Cut", "Caesar Cut", "Taper Fade", "Skin Fade", "Flat Top",
    # --- Cortes Medianos ---
    "Slick Back", "Pompadour", "Quiff", "Undercut", "Side Part",
    "Bro Flow", "Mid Part (Cortina)", "Bowl Cut", "Shaggy Cut",
    "Bob Cut", "Lob (Long Bob)", "Asymmetrical Bob", "Pageboy Cut",
    # --- Cortes Largos ---
    "Long Layers (Capas Largas)", "Feathered Hair (Cabello en Plumas)",
    "Man Bun", "Top Knot", "Long and Straight", "Long and Wavy",
    "V-Cut Layers",
    # --- Cortes con Textura y Estilo ---
    "Curly Shag", "Messy Hair", "Spiky Hair", "Fringe (Flequillo)",
    "Bangs (Flequillo Recto)", "Wavy Bob", "Afro", "Perm (Permanente)",
    "Textured Crop",
    # --- Cortes Clásicos y Retro ---
    "Mullet", "Jheri Curl", "Hi-Top Fade", "Ducktail", "Hime Cut",
    # --- Estilos con Trenzas y Rastas ---
    "Braids (Trenzas)", "Cornrows (Trenzas pegadas)", "Box Braids",
    "Dreadlocks", "Viking Braids",
    # --- Cortes de Tendencia ---
    "Wolf Cut", "Butterfly Cut", "Octopus Cut", "Jellyfish Cut",
    "Bixie Cut (Bob-Pixie)",
    # --- Cortes con Diseños ---
    "Hair Tattoo / Hair Design", "Hard Part (Línea Marcada)",
    "Mohawk", "Faux Hawk (Fohawk)"
]

# --- 5. INTERFAZ DE PESTAÑAS ---
tab_reportes, tab_analista, tab_marketing, tab_oportunidades, tab_asesor, tab_hazme_corte = st.tabs([
    "📈 Generador de Reportes", "🕵️ Analista de Datos Interactivo", "🎯 Asistente de Marketing",
    "💎 Detector de Oportunidades", "✂️ Asesor de Estilo Virtual", "🎨 Hazme un Nuevo Corte" 
])

# --- PESTAÑA 1: GENERADOR DE REPORTES ---
with tab_reportes:
    st.header("Generador de Reportes a Medida")
    st.info(f"El reporte se generará basado en las **{len(df_filtrado)} citas** que coinciden con tus filtros actuales.")
    
    def generar_analisis_reporte(resumen_str):
        if not model: return "El modelo de IA no está disponible."
        
        # 2. SE REEMPLAZA LOCALE POR BABEL
        fecha_actual = format_date(datetime.now(), format="d 'de' MMMM 'de' yyyy", locale='es')

        prompt = f"""
        Actúa como un analista de negocios para Kingdom Barber.
        Tu tarea es tomar el siguiente resumen de datos y convertirlo en un informe profesional.

        **Contexto del Informe:**
        - **Fecha de Generación:** {fecha_actual}
        - **Para:** Dirección de Kingdom Barber
        - **De:** Analista de Negocios de IA

        **Resumen de Datos (KPIs):**
        {resumen_str}

        **Estructura del Informe (Usa Markdown):**
        ### Informe de Análisis de Rendimiento
        - (Incluye la fecha, para y de que te di en el contexto)
        ---
        #### 1. Resumen Ejecutivo
        Párrafo corto con los hallazgos más críticos.
        #### 2. Observaciones Clave
        3 puntos destacando tendencias basadas en el resumen.
        #### 3. Recomendaciones Estratégicas
        2 acciones concretas basadas en las observaciones.
        """
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error al generar análisis: {e}"

    if st.button("🚀 Generar Reporte PDF", key="report_btn"):
        if df_filtrado.empty:
            st.warning("No hay datos para los filtros seleccionados.")
        else:
            with st.spinner("Analizando KPIs y consultando a la IA... 🤖"):
                total_ingresos = df_filtrado['Precio'].sum()
                total_citas = len(df_filtrado)
                ingresos_por_barbero = df_filtrado.groupby('Nombre_Completo_Barbero')['Precio'].sum().nlargest(5)
                citas_por_servicio = df_filtrado['Nombre_Servicio'].value_counts().nlargest(5)
                
                resumen_de_datos = f"""
                - Total de Citas: {total_citas}
                - Ingresos Totales: ${total_ingresos:,.0f} COP
                - Top 5 Barberos por Ingresos: {ingresos_por_barbero.to_dict()}
                - Top 5 Servicios por Cantidad: {citas_por_servicio.to_dict()}
                """
                
                analisis_ia = generar_analisis_reporte(resumen_de_datos)
            
            with st.spinner("Creando el archivo PDF... 📄"):
                contexto_reporte = {"sede": sede_seleccionada, "rango_fechas": f"{rango_fechas[0].strftime('%d/%m/%Y')} - {rango_fechas[1].strftime('%d/%m/%Y')}", "barbero": barbero_seleccionado, "servicio": servicio_seleccionado}
                pdf_bytes = generar_pdf_reporte(df_filtrado, analisis_ia, contexto_reporte)
            
            st.success("¡Reporte generado con éxito!")
            st.download_button(label="📥 Descargar Reporte PDF", data=pdf_bytes, file_name="Reporte_IA.pdf", mime="application/pdf")

# --- PESTAÑA 2: ANALISTA DE DATOS INTERACTIVO (CORREGIDA) ---
with tab_analista:
    st.header("🕵️ Chatea con tus Datos")
    st.info(f"Tengo acceso a las **{len(df_filtrado)} citas** que coinciden con tus filtros. Hazme cualquier pregunta.")
    pregunta_usuario = st.text_input("Escribe tu pregunta aquí:", placeholder="Ej: ¿Cuál es el mes de más ganancias?", key="analista_input")
    
    if st.button("🤖 Analizar y Responder", key="analista_btn"):
        if not model: st.error("Motor de IA no disponible.")
        elif not pregunta_usuario: st.warning("Por favor, escribe una pregunta.")
        elif df_filtrado.empty: st.warning("No hay datos para los filtros seleccionados.")
        else:
            with st.spinner("Generando plan de análisis... 🧠"):
                columnas = df_filtrado.columns.tolist()
                tipos_de_datos = df_filtrado.dtypes.to_string()
                
                prompt_agente = f"""
                Actúa como 'Alex', un Agente de IA experto en análisis de datos con Pandas.
                Tu objetivo es generar un script de Python para responder la pregunta del usuario analizando un DataFrame llamado `df`.
                
                **Contexto del DataFrame `df`:**
                - Contiene datos de citas de una barbería. 'Precio' es ingresos. 'Fecha' es para análisis de tiempo.

                **Reglas Estrictas:**
                1. SOLO CÓDIGO: Tu única respuesta debe ser código Python.
                2. USA `df`: El DataFrame a analizar SIEMPRE se llama `df`.
                3. IMPRIME EL RESULTADO: El código DEBE terminar con `print(resultado)`.
                4. CÓDIGO CLARO: Añade comentarios breves para explicar los pasos.
                5. FORMATO DE FECHA: Si la pregunta involucra fechas (meses, años), el resultado impreso DEBE incluir el año (ej. 'Febrero 2025').
                6. **PROVEE CONTEXTO:** Siempre que sea posible, además de la respuesta directa, imprime datos adicionales que le den contexto. Por ejemplo, si la pregunta es sobre el mes con más ganancias, el código no solo debe imprimir el mes, sino también el monto de esas ganancias.

                **Información del DataFrame:**
                - COLUMNAS: {columnas}
                - TIPOS DE DATOS: {tipos_de_datos}

                **Pregunta del Usuario:**
                "{pregunta_usuario}"
                """
                try:
                    respuesta_ia = model.generate_content(prompt_agente)
                    codigo_generado = respuesta_ia.text.strip().replace("```python", "").replace("```", "")
                    with st.expander("🔍 Ver el Plan de Análisis (código generado)"):
                        st.code(codigo_generado, language='python')
                    
                    with st.spinner("Ejecutando el análisis... ⚙️"):
                        df = df_filtrado.copy()
                        old_stdout, sys.stdout = sys.stdout, StringIO()
                        exec(codigo_generado, {'pd': pd, 'df': df})
                        resultado_analisis = sys.stdout.getvalue()
                        sys.stdout = old_stdout
                    
                    with st.spinner("Interpretando los resultados... 🗣️"):
                        prompt_interprete = f"""
                        Eres "Alex", un asistente de datos amigable y experto. Responde la pregunta del usuario de forma conversacional y completa, usando los datos del resultado del análisis. Explica el resultado de forma clara.

                        **Pregunta Original del Usuario:**
                        "{pregunta_usuario}"
                        
                        **Resultado del Código (Datos Crudos):**
                        ---
                        {resultado_analisis}
                        ---
                        
                        **Tu Respuesta Final:**
                        """
                        respuesta_final_ia = model.generate_content(prompt_interprete)
                        st.markdown("### 💡 Aquí está tu análisis:")
                        st.success(respuesta_final_ia.text)
                except Exception as e:
                    st.error("¡Oops! Ocurrió un error al procesar tu pregunta.")
                    st.exception(e)

# --- PESTAÑA 3: ASISTENTE DE MARKETING ---
with tab_marketing:
    st.header("🎯 Asistente de Marketing Inteligente")
    st.markdown("Genera ideas para tus campañas de marketing basados en los datos filtrados.")
    col1, col2 = st.columns(2)
    with col1:
        tipo_campaña = st.selectbox("Selecciona el objetivo de la campaña:", ["Atraer nuevos clientes", "Fidelizar clientes existentes", "Promocionar un servicio poco popular", "Aumentar citas en días flojos"], key="marketing_objetivo")
    with col2:
        canal_comunicacion = st.radio("Selecciona el canal:", ("WhatsApp", "Email", "Redes Sociales"), horizontal=True, key="marketing_canal")
    
    if st.button("💡 Generar Idea de Campaña", key="marketing_btn"):
        if not model: st.error("El modelo de IA no está disponible.")
        elif df_filtrado.empty: st.warning("No hay suficientes datos para generar una idea.")
        else:
            with st.spinner("Creando una campaña brillante... ✨"):
                try:
                    # 3. SE USA BABEL PARA OBTENER EL NOMBRE DEL DÍA EN ESPAÑOL
                    df_filtrado['Dia_Semana'] = pd.to_datetime(df_filtrado['Fecha']).dt.day_name(locale='es_ES.UTF-8')
                    servicio_menos_popular = df_filtrado['Nombre_Servicio'].value_counts().idxmin()
                    dia_mas_flojo = df_filtrado['Dia_Semana'].value_counts().idxmin()
                except Exception:
                    servicio_menos_popular, dia_mas_flojo = "N/A", "N/A"
                
                prompt_marketing = f"""
                Actúa como un Director Creativo para 'Kingdom Barber'. Crea un borrador para una campaña de marketing.
                **INPUTS ESTRATÉGICOS:**
                - Objetivo: {tipo_campaña}
                - Canal: {canal_comunicacion}
                - Insight 1 (Servicio a Potenciar): {servicio_menos_popular}
                - Insight 2 (Día de Baja Afluencia): {dia_mas_flojo}
                **OUTPUT REQUERIDO (Formato Markdown):**
                Usa un tono creativo y directo.
                ### Nombre de la Campaña
                - **Slogan:** Un eslogan corto y pegadizo.
                - **Público Objetivo:**
                - **Mensaje para {canal_comunicacion}:** El texto exacto.
                - **Llamada a la Acción (CTA):**
                - **Sugerencia Creativa:**
                """
                try:
                    respuesta_ia = model.generate_content(prompt_marketing)
                    st.markdown(respuesta_ia.text)
                except Exception as e:
                    st.error(f"Ocurrió un error al generar la campaña: {e}")

# --- PESTAÑA 4: DETECTOR DE OPORTUNIDADES ---
with tab_oportunidades:
    st.header("💎 Detector de Oportunidades Personalizadas")
    st.markdown("Analizaré los datos filtrados para encontrar insights de negocio accionables.")
    opciones_analisis = st.multiselect("Selecciona qué oportunidades quieres buscar:", ["Clientes en Riesgo de Abandono", "Oportunidades de Venta Cruzada (Cross-selling)", "Optimización de Servicios", "Rendimiento de Barberos"], default=["Clientes en Riesgo de Abandono"], key="oportunidades_multi")
    
    if st.button("🔍 Encontrar Oportunidades", key="oportunidades_btn"):
        if not model: st.error("El modelo de IA no está disponible.")
        elif df_filtrado.empty or not opciones_analisis: st.warning("Selecciona un área y asegúrate de que haya datos.")
        else:
            with st.spinner("Calculando insights y consultando a la IA... 💎"):
                resumen_oportunidades = f"Áreas de interés seleccionadas: {', '.join(opciones_analisis)}\n"
                
                try:
                    if "Clientes en Riesgo de Abandono" in opciones_analisis:
                        fecha_maxima = df_filtrado['Fecha'].max()
                        clientes_recientes = df_filtrado[df_filtrado['Fecha'] > (fecha_maxima - pd.Timedelta(days=90))]
                        todos_los_clientes = df_filtrado['Nombre_Completo_Cliente'].nunique()
                        clientes_recientes_unicos = clientes_recientes['Nombre_Completo_Cliente'].nunique()
                        resumen_oportunidades += f"- Total de clientes únicos en el periodo: {todos_los_clientes}\n"
                        resumen_oportunidades += f"- Clientes que han visitado en los últimos 90 días: {clientes_recientes_unicos}\n"
                    
                    prompt_oportunidad = f"""
                    Eres un consultor de negocios para 'Kingdom Barber'.
                    Analiza el siguiente resumen de datos y, para CADA área de interés, proporciona un análisis en Markdown con:
                    #### Nombre del Área
                    - **Hallazgo Clave:**
                    - **Oportunidad de Negocio:**
                    - **Acción Recomendada:**
                    
                    **Resumen de Datos:**
                    {resumen_oportunidades}
                    """
                    respuesta_ia = model.generate_content(prompt_oportunidad)
                    st.markdown(respuesta_ia.text)
                except Exception as e:
                    st.error(f"No se pudo generar el análisis de oportunidades: {e}")

# --- PESTAÑA 5: ASESOR DE ESTilo VIRTUAL (VERSIÓN COMBINADA Y MEJORADA) ---
with tab_asesor:
    st.header("✂️ Asesor de Estilo Virtual con IA")
    st.markdown("Sube una foto, recibe recomendaciones detalladas y pruébalas en la siguiente pestaña.")
    
    uploaded_file = st.file_uploader("Sube una foto donde tu rostro se vea claramente", type=["jpg", "jpeg", "png"], key="style_uploader")
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, caption="Imagen subida", width=250)
        with col2:
            if st.button("✨ ¡Recomiéndame un corte!", key="style_button"):
                if not model:
                    st.error("El modelo de IA no está disponible.")
                else:
                    with st.spinner("Analizando tus rasgos y buscando los mejores estilos... 🧐"):
                        try:
                            # Convertimos la lista de cortes en un string para el prompt
                            cortes_disponibles_str = ", ".join(sorted(lista_cortes_populares))

                            prompt_parts = [
                                f"""
                                Actúa como un estilista de élite y experto en visagismo. Tu cliente te ha mostrado una foto para que le des una asesoría de imagen completa y funcional.

                                LISTA DE CORTES VÁLIDOS PARA RECOMENDAR:
                                {cortes_disponibles_str}

                                **TU TAREA (Formato Estricto Requerido):**
                                1.  **Diagnóstico del Rostro:** Identifica la forma del rostro (ej. Ovalado, Cuadrado, Redondo, etc).
                                2.  **Recomendaciones (Top 3):** Proporciona tres recomendaciones. Para cada una, sigue EXACTAMENTE este formato detallado:

                                ### Recomendación [NÚMERO]
                                - **Nombre del Estilo:** [Elige el nombre MÁS APROPIADO de la LISTA DE CORTES VÁLIDOS].
                                - **Análisis del Estilista:** [Explica en una frase por qué este corte le favorece].
                                - **Nivel de Mantenimiento:** [Indica si es Bajo, Medio o Alto].
                                - **Productos Recomendados:** [Sugiere 1-2 productos, ej: Cera mate, pomada, aceite para barba].
                                - **Inspiración Visual:** [Proporciona un enlace de búsqueda de Google Images para este estilo].
                                - **Especificaciones para Copiar:**
                                ```
                                [Aquí, escribe especificaciones detalladas y creativas que el usuario pueda copiar y pegar. Incluye detalles sobre textura (liso, ondulado), longitud, color sugerido, tipo de desvanecido, etc. Sé específico. Por ejemplo: "Cabello ondulado con textura natural, color castaño claro con reflejos sutiles, longitud media en la parte superior, desvanecido bajo (low fade) en los lados."]
                                ```
                                """,
                                image,
                            ]
                            
                            # Usamos la misma configuración de seguridad para evitar bloqueos
                            safety_settings = {
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            }

                            response = model.generate_content(prompt_parts, safety_settings=safety_settings)
                            
                            st.divider()
                            st.markdown("### 💈 Mis recomendaciones para ti:")
                            st.info("Copia el 'Nombre del Estilo' y las 'Especificaciones' en la pestaña 'Hazme un Nuevo Corte' para generar una vista previa.")
                            st.markdown(response.text)
                            st.link_button("📅 ¡Reserva tu cita ahora!", "https://pi-web2-six.vercel.app", type="primary")
                        
                        except Exception as e:
                            st.error("¡Oops! Ocurrió un error al analizar la imagen.")
                            st.exception(e)

# --- PESTAÑA 6: HAZME UN NUEVO CORTE (CÓDIGO COMPLETO Y FINAL) ---
with tab_hazme_corte:
    st.header("🎨 Experimenta tu Nuevo Look")
    st.markdown("Sube una foto y aplica el corte de cabello que siempre has querido. ¡La IA lo hará realidad!")

    uploaded_file_corte = st.file_uploader("Sube una foto clara de tu rostro:", type=["jpg", "jpeg", "png"], key="corte_uploader")

    if uploaded_file_corte is not None:
        image_corte = Image.open(uploaded_file_corte)
        col_img, col_ops = st.columns([1, 2])

        with col_img:
            st.image(image_corte, caption="Tu Imagen Original", width=250)

        with col_ops:
            st.markdown("### ✂️ Define tu Estilo")
            
            modo_corte = st.radio("¿Cómo quieres especificar el corte?", ["Seleccionar de la lista", "Escribir libremente"], horizontal=True)
            
            corte_deseado = ""
            if modo_corte == "Seleccionar de la lista":
                corte_deseado = st.selectbox("Elige un estilo de corte:", [''] + sorted(lista_cortes_populares))
            else:
                corte_deseado = st.text_input("Describe el corte que deseas:", placeholder="Ej: Buzz Cut con desvanecido", key="input_corte_libre")
            
            especificaciones_adicionales = st.text_area(
                "Añade especificaciones (color, textura, etc.):",
                placeholder="Ej: Pelo rubio platino y liso, o rizado y castaño oscuro.",
                key="especificaciones_corte"
            )

            if st.button("✨ ¡Generar mi Nuevo Corte!", key="generar_corte_btn", type="primary"):
                if not model:
                    st.error("El modelo de IA no está disponible.")
                elif not corte_deseado:
                    st.warning("Por favor, selecciona o escribe el corte deseado.")
                else:
                    with st.spinner("¡Tu nuevo look está tomando forma! Esto puede tardar un momento... ⏳"):
                        try:
                            prompt_generacion_corte = [
    f"""
    Eres un estilista de IA. Tu tarea es visualizar un nuevo look.
    Modifica la apariencia del cabello en la imagen para aplicar un corte estilo '{corte_deseado}'.
    **Es crucial que, si la imagen contiene un rostro humano, la edición se realice como si fuera un modelo 3D o una ilustración estilizada.**
    Mantén el rostro, la expresión y la pose, pero el cabello debe transformarse.
    Considera estas especificaciones adicionales: {especificaciones_adicionales if especificaciones_adicionales else 'Ninguna.'}
    La imagen final debe ser una visualización clara del nuevo corte. No tiene que ser fotorrealista si es un rostro humano.
    """,
    image_corte,
]

                            # Define la configuración de seguridad para ser menos restrictiva
                            safety_settings = {
                                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                            }

                            # Realiza la llamada a la IA AÑADIENDO la configuración de seguridad
                            generated_response = model.generate_content(
                                prompt_generacion_corte,
                                safety_settings=safety_settings
                            )
                            
                            if generated_response.prompt_feedback.block_reason:
                                st.error("La solicitud fue bloqueada por las políticas de seguridad de la IA.")
                                st.warning(f"Razón del bloqueo: **{generated_response.prompt_feedback.block_reason.name}**")
                                st.info("Intenta con una imagen diferente o una descripción más general.")
                            else:
                                image_found = False
                                for part in generated_response.parts:
                                    if hasattr(part, 'blob') and hasattr(part.blob, 'mime_type') and part.blob.mime_type.startswith("image/"):
                                        st.success("¡Aquí está tu nuevo look!")
                                        st.image(
                                            part.blob.data,
                                            caption=f"Tu look con el corte: {corte_deseado}",
                                            use_container_width=True
                                        )
                                        st.link_button("📅 ¡Reserva tu cita ahora!", "https://pi-web2-six.vercel.app", type="primary")
                                        image_found = True
                                        break
                                
                                if not image_found:
                                    st.error("La IA no pudo generar una imagen, pero no fue por un bloqueo de seguridad.")
                                    st.warning("Respuesta del modelo:")
                                    # Es seguro acceder a .text si no fue bloqueado y no hay imagen
                                    st.markdown(f"> {generated_response.text}")
                                    
                        except ValueError as e:
                            if "response.text" in str(e):
                                st.error("La IA devolvió una respuesta completamente vacía, probablemente debido a un bloqueo de seguridad no informado.")
                                st.info("Prueba a ajustar la configuración de seguridad o modifica el prompt.")
                            else:
                                st.error("Ocurrió un error inesperado con los datos.")
                                st.exception(e)
                        except Exception as e:
                            st.error("¡Oops! Ocurrió un error general al procesar la solicitud.")
                            st.exception(e)