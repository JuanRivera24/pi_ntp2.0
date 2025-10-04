======================================================================
             KINGDOM BARBER - PANEL DE GESTIÓN Y ANÁLISIS (PI_NTP2.0)
======================================================================

📅 Documentación: NTP - Kingdom Barber  
📆 Fecha: Octubre, 2025  
👥 Autores: Juan Rivera, Andrés Vallejo, Alejandro Urrego

======================================================================
                   📘 DESCRIPCIÓN GENERAL
======================================================================

Kingdom Barber - Panel de Gestión y Análisis (pi_ntp2.0)  
Este repositorio contiene el código del Panel de Gestión y Análisis de Kingdom Barber,  
una aplicación web desarrollada en **Python** con **Streamlit**. Esta herramienta está diseñada  
para la administración del negocio y la inteligencia de negocios.

Este proyecto es un **front-end puro** que consume datos en tiempo real desde la **API Central de Java**.

======================================================================
              📖 GUÍA DE EJECUCIÓN Y MANUAL DE USO
======================================================================

-----------------------------
-- 1. REQUISITOS PREVIOS --
-----------------------------

Antes de empezar, asegúrate de tener instalado lo siguiente en tu sistema:

- Python (versión 3.8 o superior).

⚠️ **Importante:** Esta aplicación es un cliente de datos.  
Para que funcione, la API de Java (**pi_movil2.0**) debe estar ejecutándose en:  
👉 `http://localhost:8080`

-----------------------------
-- 2. INSTALACIÓN Y EJECUCIÓN --
-----------------------------

Sigue estos pasos para poner en marcha el proyecto en tu máquina local.

**Paso 1: Crear un Entorno Virtual**

Abre una terminal en la carpeta raíz del proyecto y ejecuta:

```
python -m venv .venv
```

**Paso 2: Activar el Entorno Virtual**

Windows:
```
.venv\Scripts\activate
```
(En Linux/macOS usar `source .venv/bin/activate`)

Verás que el prompt de la terminal ahora empieza con `(.venv)`.

**Paso 3: Instalar Dependencias**

Con el entorno activado, instala las librerías necesarias:

```
pip install -r requirements.txt
```

**Paso 4: Iniciar la Aplicación**

Inicia la app de Streamlit:

```
streamlit run inicio.py
```

======================================================================
                🧩 GUÍA DE MÓDULOS PRINCIPALES
======================================================================

La aplicación se divide en varias páginas accesibles desde la barra lateral izquierda.

-----------------------------
-- a) DASHBOARD --
-----------------------------

- Vista principal de análisis con KPIs: ingresos totales, número de citas, rendimiento de barberos.  
- Gráficos interactivos que se actualizan según los filtros de la barra lateral.

-----------------------------
-- b) GESTIÓN DE CITAS --
-----------------------------

- Herramienta para visualizar y filtrar el historial completo de citas (~4000 registros).  
- Filtros por sede, barbero, cliente y rango de fechas.  
- Tabla detallada y cálculo de ingresos según la selección.

-----------------------------
-- c) ASISTENTE IA --
-----------------------------

Módulo avanzado que utiliza la IA de Google (Gemini) para tareas sobre los datos filtrados:

- **Generador de Reportes:** crea informes en PDF con análisis estratégico.  
- **Analista de Datos Interactivo:** chat que responde preguntas y ejecuta código Pandas.  
- **Asistente de Marketing:** genera ideas y textos para campañas.  
- **Detector de Oportunidades:** identifica patrones y anomalías.  
- **Asesor de Estilo:** recomienda cortes de cabello a partir de una imagen.

======================================================================
                   📌 RESUMEN DEL PROYECTO
======================================================================

El Panel de Gestión de Kingdom Barber (pi_ntp2.0) es una aplicación de BI desarrollada en Python y Streamlit.  
Su propósito es ser la herramienta central de administración y análisis de datos para la barbería, ofreciendo visualizaciones, gestión histórica y un asistente de IA.

**Nota:** Es un cliente de datos puro: toda la información se consume en tiempo real desde la API Central de Java + Spring Boot, que es la única fuente de verdad.

======================================================================
                  🎯 OBJETIVOS DEL PROYECTO
======================================================================

-----------------------------
-- Objetivo Principal --
-----------------------------

Proveer una herramienta de Business Intelligence (BI) completa y fácil de usar para la toma de decisiones estratégicas, centralizando la visualización y el análisis de los datos operativos de Kingdom Barber.

-----------------------------
-- Objetivos Específicos --
-----------------------------

- Visualizar KPIs Clave: dashboard con indicadores (ingresos, citas, rendimiento de barberos).  
- Facilitar la Consulta de Datos: interfaz para filtrar y buscar en el historial completo.  
- Aprovechar la IA: integrar un asistente (Gemini) para reportes y consultas en lenguaje natural.  
- Desacoplamiento Total: cliente independiente que consume exclusivamente la API de Java.

======================================================================
                   🧠 STACK TECNOLÓGICO
======================================================================

- Lenguaje: **Python**  
- Framework Web: **Streamlit**  
- Procesamiento de Datos: **Pandas**  
- Visualización: **Plotly Express**  
- Generación de PDF: **FPDF2**  
- Inteligencia Artificial: **Google Generative AI (Gemini)**  
- Consumo de API: **requests**  
- Back-End Consumido: **API REST Java + Spring Boot** (`http://localhost:8080`)

======================================================================
           🗂️ ARQUITECTURA Y ESTRUCTURA DE CARPETAS
======================================================================

El proyecto sigue la estructura modular de Streamlit: cada página es un archivo `.py`.

```
pi_ntp2.0/
├── 📂 .streamlit/         # Configuración de Streamlit (secrets.toml)
├── 📂 assets/             # Recursos estáticos (imágenes, logos)
├── 📂 pages/              # Páginas de la aplicación (cada .py = una página)
│   ├── 📜 1_Dashboard.py
│   ├── 📜 2_Gestion_de_Citas.py
│   └── 📜 3_Asistente_IA.py
│
├── 📜 inicio.py           # Punto de entrada y bienvenida
├── 📜 data_manager.py     # Módulo para comunicación con la API Java
├── 📜 report_generator.py # Lógica para crear reportes PDF
└── 📜 requirements.txt    # Dependencias del proyecto
```

======================================================================
                  🧾 MÓDULOS PRINCIPALES (DETALLE)
======================================================================

1. **Dashboard General (1_Dashboard.py)**  
   - Fuente de datos: API Central de Java.  
   - Métricas: ingresos totales, citas registradas, servicio popular, barbero top.  
   - Gráficos: ingresos por servicio, carga de trabajo por barbero, evolución de citas.

2. **Gestión de Citas (2_Gestion_de_Citas.py)**  
   - Fuente de datos: `/historial/citas` (API Java).  
   - Funcionalidades: filtros por sede, barbero, cliente, rango de fechas; tabla detallada; cálculo de ingresos.

3. **Asistente de Inteligencia Artificial (3_Asistente_IA.py)**  
   - Fuente de datos: misma API que el Dashboard.  
   - Funciones: generador de reportes PDF, analista de datos interactivo (chat y ejecución de Pandas), asistente de marketing, detector de oportunidades, asesor de estilo virtual.

======================================================================
       🔄 FLUJO DE DATOS TÍPICO: CARGA DEL DASHBOARD
======================================================================

1. **Usuario (Streamlit):** Abre la página del Dashboard.  
2. **Front-End (`1_Dashboard.py`):** Llama a `obtener_vista_citas_completa()` en `data_manager.py`.  
3. **Gestor de Datos (`data_manager.py`):**
   - Realiza peticiones `GET` con `requests` a la API Java (ej.: `/historial/citas`, `/clientes`).  
   - Recibe respuestas en JSON.  
   - Convierte JSON a **DataFrame** (Pandas).  
   - Traduce nombres de columnas (`camelCase` → `Pascal_Case`).  
   - Realiza merges para obtener una tabla enriquecida.  
4. **Respuesta al Front-End:** `data_manager.py` devuelve el DataFrame procesado al script del dashboard.  
5. **Actualización UI:** Streamlit + Plotly Express renderizan gráficos y métricas interactivos con los datos recibidos.

======================================================================
                          📌 NOTAS FINALES
======================================================================

- Este panel es una pieza clave del ecosistema Kingdom Barber para análisis y toma de decisiones.  
- Está diseñado para escalar y admitir nuevos módulos o integraciones con modelos predictivos en el futuro.

======================================================================

