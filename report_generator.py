import pandas as pd
from fpdf import FPDF
import matplotlib.pyplot as plt
import io # Necesario para manejar imágenes en memoria

def generar_pdf_reporte(df, analisis_ia, contexto_reporte):
    """
    Genera un reporte en PDF con KPIs, análisis de IA y gráficos.

    Args:
        df (pd.DataFrame): El DataFrame filtrado con los datos.
        analisis_ia (str): El texto del análisis generado por la IA.
        contexto_reporte (dict): Un diccionario con el contexto (fechas, sede, etc.).

    Returns:
        bytes: El contenido del PDF como un objeto de bytes.
    """
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Reporte de Desempeño - Barbería', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 11)
            # Usamos multi_cell para manejar múltiples líneas y caracteres especiales
            self.multi_cell(0, 10, body)
            self.ln()

    # Creación del objeto PDF
    pdf = PDF()
    pdf.add_page()

    # Título del reporte con el contexto
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f"Reporte para: {contexto_reporte.get('sede', 'Todas las Sedes')}", 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    fecha_str = f"Desde: {contexto_reporte.get('fecha_inicio', 'N/A')} - Hasta: {contexto_reporte.get('fecha_fin', 'N/A')}"
    pdf.cell(0, 10, fecha_str, 0, 1, 'C')
    pdf.ln(10)

    # 1. KPIs
    pdf.chapter_title('Indicadores Clave de Desempeño (KPIs)')
    
    total_citas = len(df)
    total_ingresos = df['Precio'].sum()
    ingreso_promedio = df['Precio'].mean() if total_citas > 0 else 0
    
    kpi_text = (
        f"- Citas Totales: {total_citas}\n"
        f"- Ingresos Totales: ${total_ingresos:,.2f}\n"
        f"- Ingreso Promedio por Cita: ${ingreso_promedio:,.2f}"
    )
    pdf.chapter_body(kpi_text)

    # 2. Análisis de la IA
    pdf.chapter_title('Análisis y Recomendaciones (IA)')
    # Convertimos el texto a latin-1 para compatibilidad con FPDF
    analisis_ia_compatible = analisis_ia.encode('latin-1', 'replace').decode('latin-1')
    pdf.chapter_body(analisis_ia_compatible)

    # (Opcional) Si quieres añadir un gráfico, puedes hacerlo aquí.
    # Por ahora lo dejamos como placeholder para no añadir complejidad.

    # Generar el PDF en memoria y devolverlo como bytes
    # --- LA LÍNEA CLAVE DE LA SOLUCIÓN ---
    # pdf.output() con dest='S' devuelve un bytearray.
    # NO es necesario ni correcto llamar a .encode() sobre él.
    # Simplemente lo convertimos a `bytes` para asegurar compatibilidad.
    pdf_output = bytes(pdf.output())

    return pdf_output