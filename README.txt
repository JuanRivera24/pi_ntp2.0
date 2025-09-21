======================================================================
                  KINGDOM BARBER - PANEL DE GESTIÓN
======================================================================

Bienvenido al repositorio del Panel de Gestión de Kingdom Barber, una aplicación web desarrollada en Python con Streamlit, diseñada para la administración integral y el análisis de datos de una barbería. El sistema no solo ofrece herramientas de visualización y gestión, sino que incorpora un potente Asistente de Inteligencia Artificial para análisis avanzados, generación de reportes y marketing inteligente.

-----------------------------
-- ARQUITECTURA DEL PROYECTO --
-----------------------------

El proyecto sigue una estructura modular que facilita su mantenimiento y escalabilidad:

- `inicio.py`: Punto de entrada de la aplicación. Renderiza la página de bienvenida.
- `pages/`: Contiene los scripts de las diferentes secciones (Dashboard, Gestión de Citas, Asistente IA).
- `assets/`: Almacena recursos estáticos como imágenes y logos.
- `data_manager.py`: Módulo para la lógica de carga, procesamiento y filtrado de datos.
- `report_generator.py`: Script especializado en la creación de reportes en formato PDF.
- `requirements.txt`: Lista de dependencias del proyecto.

-----------------------------
--   MÓDULOS PRINCIPALES   --
-----------------------------

### 1. Dashboard General (📊)

Esta pantalla ofrece una vista global y visual del rendimiento del negocio. Permite analizar tendencias y resultados clave de forma rápida.

**Funcionalidades Principales:**

**a) Filtrado Avanzado:**
En la barra lateral izquierda encontrarás un panel de filtros que se aplican a todo el dashboard. Los filtros funcionan en cascada, de más general a más específico:
   - **Sede:** Permite ver los datos de una sede en particular o de "Todas" en conjunto.
   - **Barbero:** Muestra los barberos disponibles según la sede seleccionada. Puedes analizar a un barbero específico o a "Todos".
   - **Cliente:** Permite enfocarse en la actividad de un cliente en particular.

**b) Métricas Clave:**
En la parte superior, verás 4 indicadores que resumen el estado actual según los filtros aplicados:
   - **Ingresos Totales:** Suma total del dinero generado por las citas.
   - **Citas Registradas:** Conteo total de citas.
   - **Servicio Popular:** El servicio más demandado.
   - **Barbero Top (Ingresos):** El barbero que más ingresos ha generado.

**c) Gráficos y Análisis Visual:**
El dashboard contiene cuatro gráficos interactivos:
   - **Distribución de Ingresos por Servicio:** Un gráfico circular que muestra qué porcentaje de los ingresos totales aporta cada servicio. Ideal para saber qué servicios son los más rentables.
   - **Carga de Trabajo por Barbero:** Un gráfico de barras que compara el número de citas atendidas por cada barbero. Útil para balancear el trabajo.
   - **Ingresos Generados por Barbero:** Un gráfico de barras que muestra cuánto dinero ha generado cada barbero. Complementa al de carga de trabajo.
   - **Evolución de Citas en el Tiempo:** Un gráfico de líneas que muestra la cantidad de citas a lo largo del tiempo. Puedes cambiar la vista a "Día", "Semana" o "Mes" para identificar patrones y tendencias. Incluye una línea de promedio para comparar el rendimiento.

**d) Inventario de Productos:**
Al final de la página se muestra una tabla con el inventario de productos, cargado en tiempo real desde una API externa.

---

### 2. Gestión de Citas (🗓️)

Esta sección es la herramienta operativa para buscar, revisar y gestionar el detalle de todas las citas registradas en el sistema.

**Funcionalidades Principales:**

**a) Búsqueda y Filtrado Detallado:**
La barra lateral permite combinar múltiples filtros para encontrar citas específicas:
   - **Filtrar por Sede:** Muestra solo las citas de la ubicación seleccionada.
   - **Filtrar por Barbero:** Acota la búsqueda a un barbero en particular.
   - **Filtrar por Cliente:** Muestra el historial de citas de un solo cliente.
   - **Filtrar por Rango de Fecha:** Permite seleccionar un periodo de tiempo (inicio y fin) para ver las citas dentro de esas fechas.

**b) Tabla de Resultados:**
La tabla principal muestra todas las citas que coinciden con los filtros seleccionados, ordenada por fecha (de la más reciente a la más antigua). Incluye columnas clave como:
   - Fecha y Hora de la cita.
   - Sede, Cliente y Barbero asignados.
   - Servicio realizado y su Precio.

**c) Métrica de Ingresos:**
Sobre la tabla se muestra un indicador con la suma de los ingresos correspondientes únicamente a las citas que se están visualizando en la tabla filtrada.

---

### 3. Asistente de Inteligencia Artificial (🤖)

Este es el centro de mando para análisis avanzados y automatización. Integra varios sub-módulos especializados que utilizan IA para transformar datos en insights y acciones concretas.

**Funcionalidades del Asistente IA:**

**a) Generador de Reportes (📈):**
   - **Objetivo:** Automatizar la creación de informes ejecutivos en formato PDF.
   - **Funcionamiento:** El usuario aplica filtros (sede, barbero, fechas) y, al hacer clic, el sistema genera un documento PDF con los datos y gráficos correspondientes. Incluye un **análisis interpretativo generado por IA** que resume los hallazgos clave en lenguaje natural.

**b) Analista de Datos Interactivo (🕵️):**
   - **Objetivo:** Permitir a los usuarios "conversar" con sus datos.
   - **Funcionamiento:** Un chatbot que entiende preguntas en lenguaje natural sobre los datos de la barbería (ej: "¿Cuál fue el total de ingresos el mes pasado?"). La IA traduce la pregunta a una consulta y devuelve una respuesta precisa.

**c) Asistente de Marketing (🎯):**
   - **Objetivo:** Crear textos de marketing persuasivos y adaptados a diferentes canales.
   - **Funcionamiento:** El usuario selecciona plataforma (WhatsApp, Instagram, Email), objetivo (promoción, descuento) y detalles clave. La IA redacta un mensaje optimizado listo para ser utilizado.

**d) Detector de Oportunidades (💎):**
   - **Objetivo:** Identificar patrones ocultos y oportunidades de crecimiento.
   - **Funcionamiento:** Utiliza algoritmos para analizar el historial y detectar automáticamente oportunidades de venta cruzada, clientes en riesgo de abandono y horas de baja demanda, presentando estos insights como recomendaciones accionables.

**e) Asesor de Estilo Virtual (✂️):**
   - **Objetivo:** Ofrecer recomendaciones de estilo personalizadas.
   - **Funcionamiento:** Basado en descripciones textuales (forma de cara, tipo de cabello), la IA sugiere cortes de cabello o estilos de barba que se ajusten al perfil del cliente.

