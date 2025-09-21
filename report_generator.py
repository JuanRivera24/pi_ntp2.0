import pandas as pd
from fpdf import FPDF, HTMLMixin
import matplotlib.pyplot as plt
import io
from datetime import datetime
import numpy as np

# --- CLASE PDF (Sin cambios, ya estaba bien) ---
class PDF(FPDF, HTMLMixin):
    def header(self):
        self.set_fill_color(0, 0, 0)
        self.rect(x=10, y=8, w=33, h=33, style='F')
        try:
            self.image('assets/logo.png', x=10, y=8, w=33)
        except FileNotFoundError:
            self.set_xy(10, 8)
            self.set_font('Arial', 'B', 12)
            self.set_text_color(255, 255, 255)
            self.cell(33, 33, 'Logo', 0, 0, 'C')

        self.set_text_color(0, 0, 0)
        self.set_font('Arial', 'B', 18)
        self.cell(0, 10, 'Reporte de Desempeño', 0, 1, 'C')
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, datetime.now().strftime("Generado el %d/%m/%Y a las %H:%M:%S"), 0, 1, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def section_title(self, title):
        self.set_font('Arial', 'B', 13)
        self.set_fill_color(70, 130, 180)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f' {title}', 0, 1, 'L', fill=True)
        self.ln(5)

    def kpi_box(self, title, value, unit, width):
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

# --- CREACIÓN DE GRÁFICOS (CON EL NUEVO GRÁFICO DE HORAS PICO) ---
def crear_graficos(df):
    graficos = {}
    if df.empty:
        return graficos

    plt.style.use('seaborn-v0_8-whitegrid')

    # --- Gráfico 1: Top 5 Barberos por Ingresos ---
    try:
        top_barberos = df.groupby('Nombre_Completo_Barbero')['Precio'].sum().nlargest(5)
        if not top_barberos.empty:
            # (Código del gráfico sin cambios...)
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

    # --- Gráfico 2: Distribución de Ingresos por Servicio ---
    try:
        ingresos_servicio = df.groupby('Nombre_Servicio')['Precio'].sum()
        if not ingresos_servicio.empty:
            # (Código del gráfico sin cambios...)
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

    # --- NUEVO Gráfico 3: Horas Pico de Citas ---
    try:
        # Aseguramos que la columna 'Fecha' sea datetime
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        citas_por_hora = df['Fecha'].dt.hour.value_counts().sort_index()
        if not citas_por_hora.empty:
            buffer = io.BytesIO()
            fig, ax = plt.subplots(figsize=(10, 5))
            citas_por_hora.plot(kind='bar', ax=ax, color='#2E8B57', width=0.8) # Verde mar
            ax.set_title('Distribución de Citas por Hora del Día', fontsize=15, weight='bold')
            ax.set_xlabel('Hora del Día (formato 24h)', fontsize=12)
            ax.set_ylabel('Número de Citas', fontsize=12)
            plt.xticks(rotation=0)
            plt.tight_layout(pad=1.0)
            fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
            plt.close(fig)
            buffer.seek(0)
            graficos['citas_hora'] = buffer
    except Exception as e:
        print(f"Error generando gráfico de horas pico: {e}")

    return graficos

# --- FUNCIÓN PRINCIPAL (CON LA NUEVA TABLA DE DATOS) ---
def generar_pdf_reporte(df, analisis_ia, contexto_reporte):
    pdf = PDF()
    pdf.add_page()
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

    # --- NUEVA TABLA DE RESUMEN ---
    if not df.empty:
        pdf.section_title('Resumen de Rendimiento por Servicio')
        df_servicio_resumen = df.groupby('Nombre_Servicio').agg(
            Citas_Totales=('Nombre_Servicio', 'count'),
            Ingresos_Totales=('Precio', 'sum')
        ).sort_values(by='Ingresos_Totales', ascending=False).reset_index()
        
        # Formatear la columna de ingresos para que se vea bien
        df_servicio_resumen['Ingresos_Totales'] = df_servicio_resumen['Ingresos_Totales'].apply(lambda x: f"${x:,.2f}")

        # Convertir a HTML, añadir estilos y escribir en el PDF
        html_tabla = df_servicio_resumen.head(5).to_html(index=False, border=0, classes="dataframe")
        # Reemplazamos el estilo por defecto por uno más limpio y profesional
        html_tabla_styled = f"""
        <style>
            table.dataframe {{
                border-collapse: collapse;
                width: 100%;
                font-family: Arial;
                font-size: 11px;
            }}
            table.dataframe th {{
                background-color: #f2f2f2;
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            table.dataframe td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
        </style>
        {html_tabla}
        """
        pdf.write_html(html_tabla_styled)
        pdf.ln(10)

    pdf.section_title('Análisis y Recomendaciones de IA')
    pdf.set_text_color(0, 0, 0)
    analisis_ia_compatible = analisis_ia.encode('latin-1', 'replace').decode('latin-1')
    html_analisis = analisis_ia_compatible.replace('\n', '<br/>').replace('**', '<b>').replace('* ', '<br/>- ')
    pdf.write_html(f"<p>{html_analisis}</p>")
    pdf.ln(5)

    # Añadir página para gráficos si hay datos
    if not df.empty:
        pdf.add_page()
        pdf.section_title('Visualización de Datos')
        graficos = crear_graficos(df.copy())

        if not graficos:
            pdf.cell(0, 10, "No se pudieron generar visualizaciones.", 0, 1)
        else:
            if 'top_barberos' in graficos:
                pdf.image(graficos['top_barberos'], w=pdf.w - 30, x=15)
                pdf.ln(5)
            
            if 'ingresos_servicio' in graficos:
                pdf.image(graficos['ingresos_servicio'], w=pdf.w - 30, x=15)
                pdf.ln(5)
            
            # Colocar el nuevo gráfico
            if 'citas_hora' in graficos:
                pdf.add_page() # Añadir otra página para que no se sature
                pdf.section_title('Análisis de Horarios')
                pdf.image(graficos['citas_hora'], w=pdf.w - 30, x=15)
                pdf.ln(5)

    return bytes(pdf.output())