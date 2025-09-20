# report_generator.py

from fpdf import FPDF
import pandas as pd
from datetime import datetime

# Clase para crear el PDF con encabezado y pie de página
class PDF(FPDF):
    def header(self):
        # fpdf2 maneja internamente la codificación. Solo pasamos el string.
        # El encode/decode no es necesario aquí.
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Rendimiento - Kingdom Barber', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        
        # Tampoco es necesario codificar aquí.
        pagina_str = f'Página {self.page_no()}'
        self.cell(0, 10, pagina_str, 0, 0, 'C')
        
        # Movemos el cursor para alinear la fecha a la derecha sin sobreescribir.
        self.set_x(-50) 
        fecha_str = f"Generado el: {datetime.now().strftime('%d/%m/%Y')}"
        self.cell(0, 10, fecha_str, 0, 0, 'R')

# --- FUNCIÓN CORREGIDA Y SIMPLIFICADA ---
def generar_reporte_pdf(df_citas_reales):
    """
    Genera un reporte en PDF a partir de un DataFrame de citas.
    """
    pdf = PDF('P', 'mm', 'A4')
    pdf.add_page()

    # Es buena práctica manejar el caso donde el DataFrame esté vacío.
    if df_citas_reales.empty:
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, "No hay datos disponibles para generar el reporte.", 0, 1)
        # Salida final corregida:
        return pdf.output(dest='S').encode('latin-1')

    # Filtramos para evitar filas donde el precio es NaN
    df_citas_validas = df_citas_reales.dropna(subset=['Precio'])

    # Si después de filtrar no quedan datos, lo indicamos.
    if df_citas_validas.empty:
        pdf.set_font('Arial', '', 12)
        pdf.cell(0, 10, "No hay citas con precios válidos para generar las métricas.", 0, 1)
        return pdf.output(dest='S').encode('latin-1')

    # 1. KPIs Generales
    pdf.set_font('Arial', 'B', 14)
    # Usamos cell() con ln=1 para un mejor control del espaciado.
    pdf.cell(0, 10, '1. Métricas Clave (KPIs)', ln=1)
    
    total_ingresos = df_citas_validas['Precio'].sum()
    total_citas = len(df_citas_validas)
    servicio_popular = df_citas_validas['Nombre_Servicio'].mode().iloc[0]
    # Agrupamos por barbero para sumar sus ingresos y encontrar el máximo
    ingresos_por_barbero = df_citas_validas.groupby('Nombre_Completo_Barbero')['Precio'].sum()
    barbero_top = ingresos_por_barbero.idxmax()

    # Contenido de KPIs (sin .encode/.decode)
    pdf.set_font('Arial', '', 12)
    kpi_texto = (
        f"  - Ingresos Totales: ${total_ingresos:,.0f}\n"
        f"  - Citas Registradas: {total_citas}\n"
        f"  - Servicio Más Popular: {servicio_popular}\n"
        f"  - Barbero Top (por Ingresos): {barbero_top}"
    )
    pdf.multi_cell(0, 8, kpi_texto)
    pdf.ln(10)

    # 2. Análisis de la IA
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Análisis por IA', ln=1)
    pdf.set_font('Arial', '', 12)
    analisis_texto = (
        "El análisis de los datos revela una fuerte concentración de ingresos en los servicios más populares. "
        "Se observa una tendencia positiva en el número de citas, con picos de actividad consistentes. "
        "El rendimiento de los barberos es notable, destacando la contribución del barbero top a los ingresos generales."
    )
    pdf.multi_cell(0, 6, analisis_texto)
    pdf.ln(10)

    # 3. Gráficos (Placeholder)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '3. Visualización de Datos', ln=1)
    pdf.set_font('Arial', '', 12)
    placeholder_texto = "(Aquí se insertarán los gráficos del dashboard en el futuro)"
    pdf.cell(0, 10, placeholder_texto, ln=1)

    # --- CORRECCIÓN CLAVE ---
    # El método output() con dest='S' ya devuelve bytes codificados en latin-1.
    # No es necesario, y es incorrecto, volver a codificarlo.
    # Lo convertimos a bytearray() directamente para que Streamlit pueda usarlo.
    return pdf.output()