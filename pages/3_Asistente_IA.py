import streamlit as st
import pandas as pd
from data_manager import obtener_vista_citas_completa
from report_generator import generar_pdf_reporte
import google.generativeai as genai
import traceback
from io import StringIO
import sys
from PIL import Image

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
tab_reportes, tab_analista, tab_marketing, tab_oportunidades, tab_asesor = st.tabs([
    "📈 Generador de Reportes", 
    "🕵️ Analista de Datos Interactivo", 
    "🎯 Asistente de Marketing",
    "💎 Detector de Oportunidades",
    "✂️ Asesor de Estilo Virtual" # <-- AÑADIR ESTA NUEVA PESTAÑA
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

import pandas as pd
# Necesitaremos una forma de ejecutar código de forma segura.
# Por simplicidad, usaremos exec(), pero en producción se recomienda un sandbox.

# --- PESTAÑA 2: AGENTE DE DATOS INTERACTIVO (CON EXPANDER PARA EL CÓDIGO) ---
with tab_analista:
    st.header("🕵️ Chatea con tus Datos")
    st.markdown("Soy un agente de datos. Hazme cualquier pregunta y generaré el código para encontrar la respuesta.")
    
    st.info(f"Tengo acceso a las **{len(df_filtrado)} citas** que coinciden con tus filtros. ¡Desafíame con tu pregunta!")

    st.session_state.df_filtrado = df_filtrado

    pregunta_usuario = st.text_input(
        "Escribe tu pregunta aquí:", 
        placeholder="Ej: ¿Cuál es el servicio que generó menos ingresos en Mayo?"
    )

    if st.button("🤖 Analizar y Responder"):
        if not model:
            st.error("No puedo conectarme con mi motor de IA en este momento.")
        elif not pregunta_usuario:
            st.warning("Por favor, escribe una pregunta para que pueda analizar los datos.")
        elif st.session_state.df_filtrado.empty:
            st.warning("No hay datos disponibles para los filtros que seleccionaste.")
        else:
            with st.spinner("Entendiendo tu pregunta y generando un plan de análisis... 🧠"):
                
                columnas = st.session_state.df_filtrado.columns.tolist()
                tipos_de_datos = st.session_state.df_filtrado.dtypes.to_string()
                
                prompt_agente = f"""
                Eres "Alex", un Agente de IA experto en análisis de datos con Pandas.
                Tu objetivo es responder a la pregunta del usuario generando código Python para analizar un DataFrame llamado `df`.

                **REGLAS ESTRICTAS:**
                1.  **SOLO CÓDIGO:** Tu respuesta debe ser únicamente un bloque de código Python. Sin explicaciones.
                2.  **USA EL DATAFRAME `df`:** El DataFrame a analizar se llama `df`.
                3.  **DEVUELVE UN RESULTADO COMPLETO:** El resultado final no debe ser solo un número o un ID. Debe ser un resultado informativo que ayude a responder la pregunta.
                4.  **IMPRIME EL RESULTADO:** El código DEBE terminar con `print(resultado)` para mostrar la salida.
                5.  **COLUMNAS DISPONIBLES:** {columnas}
                6.  **TIPOS DE DATOS:** Asegúrate de usar las columnas de fecha (`Fecha`) correctamente.
                    {tipos_de_datos}

                **PREGUNTA DEL USUARIO:**
                "{pregunta_usuario}"

                **Ejemplos de cómo pensar:**
                - Pregunta: "¿Quién es el cliente más fiel (con más citas)?"
                  Código correcto:
                  `citas_por_cliente = df.groupby('Nombre_Completo_Cliente')['ID_Cita'].count()`
                  `cliente_fiel = citas_por_cliente.idxmax()`
                  `numero_citas = citas_por_cliente.max()`
                  `resultado = f"El cliente más fiel es {{cliente_fiel}} con {{numero_citas}} citas."`
                  `print(resultado)`
                
                - Pregunta: "¿Mes de menos ganancias?"
                  Código correcto:
                  `df['Fecha'] = pd.to_datetime(df['Fecha'])`
                  `df['Mes'] = df['Fecha'].dt.to_period('M')`
                  `ganancias_mes = df.groupby('Mes')['Precio'].sum()`
                  `resultado = ganancias_mes.nsmallest(1)`
                  `print(resultado)`
                
                Ahora, genera el código Python para responder la pregunta del usuario.
                """

                try:
                    # 1. La IA genera el código
                    respuesta_ia = model.generate_content(prompt_agente)
                    codigo_generado = respuesta_ia.text.strip().replace("```python", "").replace("```", "")
                    
                    # --- ¡AQUÍ ESTÁ EL CAMBIO! ---
                    # Usamos st.expander para mostrar el código generado de forma opcional.
                    with st.expander("🔍 Ver el Plan de Análisis (código generado por la IA)"):
                        st.code(codigo_generado, language='python')

                    # 2. Ejecutamos el código
                    with st.spinner("Ejecutando el análisis... ⚙️"):
                        df = st.session_state.df_filtrado
                        old_stdout = sys.stdout
                        redirected_output = sys.stdout = StringIO()
                        
                        pd_context = {'pd': pd, 'df': df}
                        exec(codigo_generado, pd_context)
                        
                        sys.stdout = old_stdout
                        resultado_analisis = redirected_output.getvalue()

                    # 3. La IA interpreta el resultado
                    with st.spinner("Interpretando los resultados... 🗣️"):
                        prompt_interprete = f"""
                        Eres "Alex", un asistente amigable.
                        Basado en la pregunta original y el resultado del análisis, formula una respuesta clara y directa.

                        Pregunta Original: "{pregunta_usuario}"
                        Resultado del Análisis:
                        ---
                        {resultado_analisis}
                        ---

                        Tu respuesta final:
                        """
                        respuesta_final_ia = model.generate_content(prompt_interprete)
                        st.markdown("### 💡 Aquí está tu análisis:")
                        st.success(respuesta_final_ia.text)

                except Exception as e:
                    st.error("¡Oops! Ocurrió un error. Puede que la pregunta sea muy ambigua o el código generado haya fallado.")
                    st.exception(e)

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

# --- ¡NUEVA PESTAÑA! 4: DETECTOR DE OPORTUNIDADES (VERSIÓN MEJORADA) ---
with tab_oportunidades:
    st.header("💎 Detector de Oportunidades Personalizadas")
    st.markdown("Selecciona las áreas de interés y analizaré los datos para encontrar insights accionables.")

    # Opciones de análisis que el usuario puede seleccionar
    opciones_analisis = st.multiselect(
        label="Selecciona qué tipo de oportunidades quieres buscar:",
        options=[
            "Clientes en Riesgo de Abandono",
            "Oportunidades de Venta Cruzada (Cross-selling)",
            "Optimización de Servicios (Populares y no Populares)",
            "Rendimiento de Barberos y Potencial de Capacitación",
            "Mejorar Días y Horas de Baja Demanda"
        ],
        default=[ # Podemos pre-seleccionar algunas para guiar al usuario
            "Clientes en Riesgo de Abandono",
            "Optimización de Servicios (Populares y no Populares)"
        ]
    )

    if st.button("🔍 Encontrar Oportunidades Seleccionadas"):
        if not model:
            st.error("El modelo de IA no está disponible.")
        elif df_filtrado.empty:
            st.warning("No hay suficientes datos para detectar oportunidades.")
        elif not opciones_analisis:
            st.warning("Por favor, selecciona al menos un área de interés para analizar.")
        else:
            with st.spinner("Buscando insights valiosos en los datos... 💎"):
                try:
                    # Siempre es buena práctica asegurar que la columna de fecha es datetime
                    df_filtrado['Fecha'] = pd.to_datetime(df_filtrado['Fecha'])
                    
                    # Generamos un CONTEXTO GENERAL con datos clave.
                    # La IA usará estos datos para responder a las peticiones específicas.
                    datos_clave_str = ""
                    try:
                        # 1. Clientes
                        fecha_maxima = df_filtrado['Fecha'].max()
                        clientes_recientes = df_filtrado[df_filtrado['Fecha'] > (fecha_maxima - pd.Timedelta(days=90))]
                        todos_los_clientes = df_filtrado['Nombre_Completo_Cliente'].dropna().unique()
                        clientes_recientes_unicos = clientes_recientes['Nombre_Completo_Cliente'].dropna().unique()
                        clientes_en_riesgo = [c for c in todos_los_clientes if c and c not in clientes_recientes_unicos]
                        datos_clave_str += f"- Clientes en Riesgo (no han visitado en 90 días): {len(clientes_en_riesgo)} clientes.\n"

                        # 2. Servicios
                        servicios_populares = df_filtrado['Nombre_Servicio'].value_counts().nlargest(3).index.tolist()
                        servicios_impopulares = df_filtrado['Nombre_Servicio'].value_counts().nsmallest(3).index.tolist()
                        datos_clave_str += f"- Servicios más populares: {', '.join(servicios_populares)}.\n"
                        datos_clave_str += f"- Servicios menos populares: {', '.join(servicios_impopulares)}.\n"

                        # 3. Rendimiento Barberos
                        ticket_promedio_barbero = df_filtrado.groupby('Nombre_Completo_Barbero')['Precio'].mean().sort_values(ascending=False)
                        datos_clave_str += f"- Barberos con mayor ticket promedio: {ticket_promedio_barbero.head(1).index[0]} (${ticket_promedio_barbero.head(1).values[0]:.2f}).\n"
                        
                        # 4. Días de la semana
                        dia_mas_flojo = df_filtrado['Fecha'].dt.day_name().value_counts().idxmin()
                        datos_clave_str += f"- Día de la semana con menos citas: {dia_mas_flojo}.\n"

                    except Exception as e:
                        datos_clave_str += f"No se pudieron calcular todos los datos clave. Error: {e}\n"
                    
                    # Creamos el prompt para la IA
                    prompt_oportunidad = f"""
                    Eres "Alex", un estratega de negocios experto para una cadena de barberías.
                    Tu tarea es analizar un conjunto de datos y generar estrategias accionables basadas en las áreas de interés seleccionadas por el usuario.

                    **DATOS CLAVE RESUMIDOS:**
                    {datos_clave_str}

                    **ÁREAS DE INTERÉS SELECCIONADAS POR EL USUARIO:**
                    - {', '.join(opciones_analisis)}

                    **INSTRUCCIONES:**
                    Para CADA una de las áreas de interés seleccionadas, proporciona:
                    1.  **El Hallazgo Principal:** ¿Qué dicen los datos sobre esta área? (Ej: "Hemos identificado 50 clientes que no han regresado en 3 meses").
                    2.  **La Oportunidad Estratégica:** ¿Por qué es esto importante? ¿Qué se puede ganar? (Ej: "Recuperar a estos clientes podría aumentar los ingresos recurrentes en un 15%").
                    3.  **Una Acción Concreta y Creativa:** Sugiere un paso claro y práctico para aprovechar la oportunidad. (Ej: "Lanzar una campaña de WhatsApp 'Te Extrañamos' con un 20% de descuento en su servicio favorito").

                    Usa Markdown para formatear tu respuesta. Usa un título (##) para cada área de interés seleccionada.
                    """

                    # Generar y mostrar la respuesta de la IA
                    respuesta_ia = model.generate_content(prompt_oportunidad)
                    st.markdown(respuesta_ia.text)

                except Exception as e:
                    st.error(f"No se pudo generar el análisis de oportunidades: {e}")
                    st.exception(e)

# --- ¡NUEVA PESTAÑA! 5: ASESOR DE ESTILO VIRTUAL (CON LINKS A GOOGLE Y BOTÓN DE CITA) ---
with tab_asesor:
    st.header("✂️ Asesor de Estilo Virtual con IA")
    st.markdown("Sube una foto de tu rostro y te recomendaré los mejores cortes de cabello para ti, basándome en la forma de tu cara.")

    # Importaciones necesarias solo para esta pestaña
    from PIL import Image
    import io
    from urllib.parse import quote_plus

    # Widget para subir la imagen
    uploaded_file = st.file_uploader(
        "Sube una foto donde tu rostro se vea claramente",
        type=["jpg", "jpeg", "png"],
        key="style_uploader"  # Usamos una 'key' única para este uploader
    )

    if uploaded_file is not None:
        # Convertir el archivo subido a un objeto de imagen
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        # Mostrar la imagen en una columna para mejor distribución
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(image, caption="Imagen subida", width=250)

        with col2:
            st.write("") # Espacio para alinear
            st.write("") # Espacio para alinear
            if st.button("✨ ¡Recomiéndame un corte!", key="style_button"):
                if not model:
                    st.error("El modelo de IA no está disponible.")
                else:
                    with st.spinner("Analizando tus rasgos y buscando referencias... 🧐"):
                        try:
                            # --- Prompt mejorado que ahora pide links de búsqueda en Google ---
                            prompt_parts = [
                                "Eres un estilista y barbero experto en visagismo y tendencias de moda masculina.",
                                "Analiza la imagen para identificar la forma del rostro de la persona (ej: ovalado, redondo, cuadrado).",
                                "Basado en esa forma, recomienda 3 cortes de cabello masculinos que le favorecerían.",
                                "Para cada recomendación, incluye:",
                                "1. **Nombre del Corte:** (Ej: 'Undercut', 'Corte Pompadour', 'Buzz Cut').",
                                "2. **Por qué le favorece:** Explica brevemente cómo el corte complementa su rostro.",
                                "3. **Nivel de Mantenimiento:** (Bajo, Medio, Alto).",
                                "4. **Referencia Visual:** Crea un link de búsqueda en Google para el nombre del corte. El formato debe ser Markdown, así: [Buscar 'Nombre del Corte' en Google](URL_de_busqueda).",
                                "Sé profesional y amigable. Formatea tu respuesta en Markdown.",
                                image,
                            ]

                            response = model.generate_content(prompt_parts)
                            st.divider()
                            st.markdown("### 💈 Aquí tienes mis recomendaciones:")
                            st.markdown(response.text)

                            # --- ¡NUEVO! Botón para reservar cita ---
                            st.link_button("📅 ¡Reserva tu cita ahora!", "http://localhost:3000", type="primary")

                        except Exception as e:
                            st.error("¡Oops! Ocurrió un error al analizar la imagen.")
                            st.exception(e)
    else:
        st.info("Esperando a que subas una imagen para comenzar el análisis.")