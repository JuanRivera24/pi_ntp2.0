import streamlit as st
import data_manager
from report_generator import generar_reporte_pdf
from datetime import datetime

# --- Configuración de la página ---
st.set_page_config(page_title="Asistente IA", page_icon="🤖", layout="wide")
st.title("🤖 Asistente de Inteligencia Artificial")
st.write("Utiliza el poder de la IA para obtener insights, generar reportes y crear campañas de marketing.")

# Cargar datos
df_citas_completa = data_manager.obtener_vista_citas_completa()
# Los KPIs ya no son necesarios aquí, la función del reporte los calcula
# kpis = data_manager.calcular_kpis(df_citas_completa)

# Inicializar estado de sesión para el reporte
if 'pdf_report' not in st.session_state:
    st.session_state.pdf_report = None

# --- Pestañas de funcionalidades ---
tab1, tab2, tab3 = st.tabs(["📄 Generador de Reportes", "🔍 Analista de Datos Interactivo", "💡 Asistente de Marketing"])

with tab1:
    st.header("Crea documentos profesionales con el resumen del rendimiento del negocio.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Configuración del Reporte")
        report_type = st.selectbox(
            "Selecciona el tipo de reporte que deseas generar:",
            ("Reporte de Rendimiento General",) # Más tipos pueden ser añadidos aquí
        )

        if st.button("Generar Reporte PDF"):
            with st.spinner("Generando reporte..."):
                # --- LLAMADA CORREGIDA ---
                # Ahora pasamos el DataFrame completo
                st.session_state.pdf_report = generar_reporte_pdf(df_citas_completa)
            st.success("¡Tu reporte ha sido generado con éxito!")

    with col2:
        st.subheader("Previsualización y Descarga")
        if st.session_state.pdf_report:
            # Construir el nombre del archivo con la fecha actual
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            nombre_archivo = f"Reporte_Rendimiento_{fecha_actual}.pdf"

            st.download_button(
                label="Descargar Reporte PDF",
                data=bytes(st.session_state.pdf_report),
                file_name=nombre_archivo,
                mime="application/pdf"
            )
            st.info("Haz clic en el botón de arriba para descargar tu reporte.")
        else:
            st.info("Genera un reporte para poder descargarlo.")

with tab2:
    st.header("Interactúa con tus datos")
    st.write("Próximamente: Haz preguntas en lenguaje natural sobre tus clientes, citas y rendimiento.")
    st.info("Funcionalidad en desarrollo.")

with tab3:
    st.header("Crea campañas de marketing inteligentes")
    st.write("Próximamente: Genera ideas para campañas, segmenta clientes y redacta mensajes de marketing.")
    st.info("Funcionalidad en desarrollo.")