import pandas as pd
from fpdf import FPDF, HTMLMixin
import matplotlib.pyplot as plt
import io
from datetime import datetime
import numpy as np

# --- CLASE PDF CORREGIDA CON MEJORAS VISUALES ---
class PDF(FPDF, HTMLMixin):
    def header(self):
        # --- SOLUCIÓN AL LOGO ---
        # 1. Dibuja un rectángulo negro como fondo para el logo.
        self.set_fill_color(0, 0, 0) # Color negro
        self.rect(x=10, y=8, w=33, h=33, style='F') # Dibuja el cuadrado

        # 2. Intenta colocar el logo encima del cuadrado.
        #    Asegúrate de que tu logo sea PNG con transparencia para que se vea bien.
        try:
            self.image('assets/logo.png', x=10, y=8, w=33)
        except FileNotFoundError:
            # Si no hay logo, muestra un texto placeholder sobre el fondo negro.
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 12)
            self.set_text_color(255, 255, 255) # Texto blanco
            self.cell(33, 33, 'Logo', 0, 0, 'C')

        # Título del reporte (reseteamos colores)
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'Reporte de Desempeño', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M:%S"), 0, 1, 'C')
        self.ln(20) # Aumentamos el espacio para que no se solape con el logo

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        # --- SOLUCIÓN AL TEXTO BLANCO ---
        self.set_font('Arial', 'B', 13)
        self.set_fill_color(70, 130, 180) # Azul acero
        self.set_text_color(255, 255, 255) # Texto blanco (Ahora sí se verá sobre el fondo azul)
        self.cell(0, 10, f' {title}', 0, 1, 'L', fill=True)
        self.ln(5)

    def kpi_box(self, title, value, unit, width):
        # Reseteamos el color del texto a negro para los KPIs
        self.set_text_color(0, 0, 0)
        self.set_font('Arial', '', 11)
        self.set_fill_color(240, 240, 240)
        
        x = self.get_x()
        y = self.get_y()
        
        self.rect(x, y, width, 20, 'DF')
        
        self.cell(width, 8, title, 0, 1, 'C')
        self.set_font('Arial', 'B', 13)
        self.set_xy(x, y + 8)
        self.cell(width, 10, f'{value} {unit}', 0, 1, 'C')
        
        self.set_y(y)
        self.set_x(x + width)

# --- CREACIÓN DE GRÁFICOS (Sin cambios, ya funcionaba bien) ---
def crear_graficos(df):
    graficos = {}
    if df.empty:
        return graficos

    plt.style.use('seaborn-v0_8-whitegrid')

    try:
        top_barberos = df.groupby('Nombre_Completo_Barbero')['Precio'].sum().nlargest(5)
        if not top_barberos.empty:
            buffer = io.BytesIO()
            fig, ax = plt.subplots(figsize=(10, 5))
            top_barberos.sort_values().plot(kind='barh', ax=ax, color='#4682B4')
            ax.set_title('Top 5 Barberos por Ingresos', fontsize=15, weight='bold')
            ax.set_xlabel('Ingresos Totales ($)', fontsize=12)
            ax.set_ylabel('')
            plt.tight_layout(pad=1.0)
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)
            graficos['top_barberos'] = buffer
    except Exception as e:
        print(f"Error generando gráfico de barberos: {e}")

    try:
        ingresos_servicio = df.groupby('Nombre_Servicio')['Precio'].sum()
        if not ingresos_servicio.empty:
            buffer = io.BytesIO()
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.Pastel1(np.arange(len(ingresos_servicio)))
            wedges, texts, autotexts = ax.pie(
                ingresos_servicio, autopct='%1.1f%%', startangle=140, colors=colors, pctdistance=0.85
            )
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig.gca().add_artist(centre_circle)
            ax.set_title('Distribución de Ingresos por Servicio', fontsize=15, weight='bold')
            ax.legend(wedges, ingresos_servicio.index, title="Servicios", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            plt.tight_layout(pad=1.0)
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)
            graficos['ingresos_servicio'] = buffer
    except Exception as e:
        print(f"Error generando gráfico de servicios: {e}")

    return graficos

# --- FUNCIÓN PRINCIPAL (Aseguramos reseteo de colores) ---
def generar_pdf_reporte(df, analisis_ia, contexto_reporte):
    pdf = PDF()
    pdf.add_page()
    
    # Reseteamos el color de texto por si acaso
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 8, f"Sede: {contexto_reporte.get('sede', 'N/A')}", 0, 1)
    pdf.set_font('Arial', '', 11)
    pdf.cell(0, 8, f"Periodo Analizado: {contexto_reporte.get('rango_fechas', 'N/A')}", 0, 1)
    pdf.ln(5)

    pdf.section_title('Indicadores Clave (KPIs)')
    total_citas = len(df)
    total_ingresos = df['Precio'].sum()
    ingreso_promedio = df['Precio'].mean() if total_citas > 0 else 0
    
    kpi_width = pdf.w / 3.2
    pdf.kpi_box("Citas Totales", f"{total_citas}", "", kpi_width)
    pdf.kpi_box("Ingresos Totales", f"${total_ingresos:,.2f}", "", kpi_width)
    pdf.kpi_box("Ingreso Promedio", f"${ingreso_promedio:,.2f}", "/ Cita", kpi_width)
    pdf.ln(25)

    pdf.section_title('Análisis y Recomendaciones de IA')
    pdf.set_text_color(0, 0, 0) # Aseguramos texto negro
    analisis_ia_compatible = analisis_ia.encode('latin-1', 'replace').decode('latin-1')
    html_analisis = analisis_ia_compatible.replace('\n', '<br/>').replace('**', '<b>').replace('* ', '<br/>- ')
    pdf.write_html(f"<p>{html_analisis}</p>")
    pdf.ln(5)

    pdf.add_page()
    pdf.section_title('Visualización de Datos')
    graficos = crear_graficos(df.copy())

    if not graficos:
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, "No hay suficientes datos para generar visualizaciones.", 0, 1)
    else:
        if 'top_barberos' in graficos:
            pdf.image(graficos['top_barberos'], w=pdf.w - 30, x=15)
            pdf.ln(5)
        
        if 'ingresos_servicio' in graficos:
            pdf.image(graficos['ingresos_servicio'], w=pdf.w - 30, x=15)
            pdf.ln(5)

    return bytes(pdf.output())