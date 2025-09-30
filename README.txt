======================================================================
                  KINGDOM BARBER - PANEL DE GESTIÓN
======================================================================

📖 DESCRIPCIÓN GENERAL
----------------------

Bienvenido al repositorio del **Panel de Gestión de Kingdom Barber**, 
una aplicación web desarrollada en **Python con Streamlit**, diseñada 
para la administración integral y el análisis de datos de una barbería.  

El sistema ofrece herramientas de visualización y gestión que consumen 
la **API Central (Node.js + Express)**, e incorpora un potente 
**Asistente de Inteligencia Artificial** y un módulo adicional de 
**análisis con datasets abiertos de Colombia**.

======================================================================
                  🏗️ ARQUITECTURA DEL PROYECTO
======================================================================

El proyecto sigue una estructura modular que facilita mantenimiento y 
escalabilidad:

- `inicio.py`: Punto de entrada de la aplicación (pantalla de bienvenida).
- `pages/`: Scripts de cada sección (Dashboard, Gestión de Citas, IA, Datasets).
- `assets/`: Recursos estáticos (imágenes, logos).
- `data_manager.py`: Manejo de comunicación con la API y filtrado de datos.
- `report_generator.py`: Generación de reportes en PDF.
- `requirements.txt`: Lista de dependencias.

======================================================================
                  ✨ MÓDULOS PRINCIPALES
======================================================================

-----------------------------
-- 1. DASHBOARD GENERAL (📊) --
-----------------------------

- Vista global del rendimiento del negocio.  
- **Fuente de datos:** API Central (Node.js).  
- Métricas clave: ingresos totales, citas registradas, servicio más 
  popular, barbero top.  
- Gráficos interactivos:  
  - Ingresos por servicio (circular).  
  - Carga de trabajo por barbero (barras).  
  - Ingresos por barbero (barras).  
  - Evolución de citas en el tiempo (líneas).  

-----------------------------
-- 2. GESTIÓN DE CITAS (🗓️) --
-----------------------------

- Herramienta operativa para consultar, filtrar y gestionar citas.  
- **Fuente de datos:** API Central (Node.js).  
- Funcionalidades:  
  - Filtro por sede, barbero, cliente y rango de fechas.  
  - Tabla de citas (ordenadas por fecha).  
  - Cálculo de ingresos en base a citas filtradas.  

-----------------------------
-- 3. ASISTENTE DE INTELIGENCIA ARTIFICIAL (🤖) --
-----------------------------

- Submódulos especializados en análisis y automatización.  
- **Fuente de datos:** API Central (ya no se usan CSV locales).  

**Funciones principales:**  
- Generador de reportes (PDF con análisis IA).  
- Chatbot analista de datos.  
- Asistente de marketing multicanal.  
- Detector de oportunidades (patrones ocultos, ventas cruzadas).  
- Asesor de estilo virtual (recomendaciones personalizadas).  

-----------------------------
-- 4. ANÁLISIS DE DATASETS ABIERTOS (📂) --
-----------------------------

- Módulo nuevo para explorar datos abiertos sobre peluquerías y 
  salones de belleza en Colombia.  
- **Fuente de datos:** Datasets públicos (CSV online).  

**Características:**  
- Limpieza y normalización de columnas.  
- Dashboards con métricas clave a nivel nacional, regional y local.  
- Filtros dinámicos por municipio, barrio y establecimiento.  
- Conclusiones automáticas generadas a partir de los filtros.  
- Visualizaciones interactivas (bar charts, métricas, tablas).  

======================================================================
               🛠️ TECNOLOGÍAS Y DEPENDENCIAS
======================================================================

- **Lenguaje:** Python  
- **Framework:** Streamlit  
- **Visualización:** Plotly Express  
- **Procesamiento:** Pandas, Regex  
- **Reportes PDF:** ReportLab  
- **Inteligencia Artificial:** Modelos de análisis de texto y datos  
- **Consumo de API:** Peticiones HTTP a API Central (Node.js)  
- **Datasets:** Integración con datos abiertos de Colombia (datos.gov.co)  

======================================================================
                   ✅ RESUMEN DE FUNCIONALIDADES
======================================================================

- **Dashboard conectado a la API** con métricas y KPIs clave.  
- **Gestión de citas** con filtros avanzados y cálculo de ingresos.  
- **Asistente IA** con submódulos de análisis, reportes y marketing.  
- **Explorador de datasets abiertos** con conclusiones dinámicas y gráficos.  
- **Arquitectura modular y escalable** lista para extenderse con más módulos.  

======================================================================
