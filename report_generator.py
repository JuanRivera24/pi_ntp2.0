import pandas as pd
from fpdf import FPDF, HTMLMixin
from datetime import datetime
from babel.dates import format_date

# --- Configuración de Estilo ---
COLOR_ORO = '#D4AF37'

class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_fill_color(30, 30, 30)
        self.rect(0, 0, 210, 40, 'F')
        try:
            self.image('assets/Logo.png', x=10, y=8, w=33)
        except RuntimeError:
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 12); self.set_text_color(255, 255, 255); self.cell(33, 33, 'Logo', 0, 0, 'C')

        self.set_y(15)
        self.set_font('Arial', 'B', 22); self.set_text_color(212, 175, 55)
        self.cell(0, 10, 'Reporte de Desempeño', 0, 1, 'C')
        
        self.set_font('Arial', '', 10); self.set_text_color(150, 150, 150)
        now = datetime.now()
        fecha_formateada = format_date(now, format='d MMMM yyyy', locale='es')
        hora_formateada = now.strftime('%H:%M:%S')
        fecha_str = f"Generado el {fecha_formateada} a las {hora_formateada}"
        self.cell(0, 8, fecha_str, 0, 1, 'C')
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(40, 40, 40)
        self.cell(0, 6, title, 0, 1, 'L')
        self.set_draw_color(212, 175, 55)
        self.line(self.get_x(), self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(8)

    def kpi_box(self, title, value, unit, width):
        self.set_font('Arial', '', 11); self.set_text_color(100, 100, 100)
        self.set_fill_color(245, 245, 245); self.set_draw_color(220, 220, 220)
        x = self.get_x(); y = self.get_y()
        self.rect(x, y, width, 22, 'DF')
        self.cell(width, 10, title, 0, 1, 'C')
        self.set_font('Arial', 'B', 16); self.set_text_color(50, 50, 50)
        self.set_xy(x, y + 10)
        self.cell(width, 10, f'{value}{unit}', 0, 1, 'C')
        self.set_y(y)
        self.set_x(x + width)

def generar_pdf_reporte(df, analisis_ia, contexto_reporte):
    pdf = PDF()
    pdf.add_page()
    
    pdf.set_font('Arial', 'B', 11); pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, f"Filtros Aplicados - Sede: {contexto_reporte.get('sede', 'N/A')}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Periodo Analizado: {contexto_reporte.get('rango_fechas', 'N/A')}", 0, 1)
    pdf.ln(5)

    pdf.section_title('Indicadores Clave de Rendimiento (KPIs)')
    total_citas = len(df.dropna(subset=['ID_Cita']))
    total_ingresos = df['Precio'].sum()
    ingreso_promedio = df['Precio'].mean() if total_citas > 0 else 0
    
    kpi_width = (pdf.w - pdf.l_margin - pdf.r_margin - 10) / 3
    pdf.kpi_box("Citas Totales", f"{total_citas}", "", kpi_width); pdf.set_x(pdf.get_x() + 5)
    pdf.kpi_box("Ingresos Totales", f"${total_ingresos:,.0f}", "", kpi_width); pdf.set_x(pdf.get_x() + 5)
    pdf.kpi_box("Ingreso Promedio", f"${ingreso_promedio:,.0f}", "/ Cita", kpi_width)
    pdf.ln(28)

    pdf.section_title('Análisis y Recomendaciones de IA')
    analisis_ia_compatible = analisis_ia.encode('latin-1', 'ignore').decode('latin-1')
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 5, analisis_ia_compatible)
    pdf.ln(10)

    # La sección de Visualización de Datos ha sido eliminada.
            
    return pdf.output(dest='S')