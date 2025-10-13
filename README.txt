======================================================================
       📊 KINGDOM BARBER - PANEL DE GESTIÓN Y ANÁLISIS (PI_NTP)
======================================================================

📘 Documentación: NTP - Kingdom Barber  
📆 Fecha: Octubre, 2025  
👥 Autores: Juan Rivera, Andrés Vallejo, Alejandro Urrego  

======================================================================
                         📖 DESCRIPCIÓN GENERAL
======================================================================

Este repositorio contiene el código del **Panel de Gestión y Análisis**
de Kingdom Barber — una aplicación de **Inteligencia de Negocios (BI)**  
desarrollada íntegramente en **Python con Streamlit**.

El sistema permite visualizar, analizar y gestionar los datos del negocio,
además de incorporar un **Asistente de Inteligencia Artificial (IA)**
para generar reportes, responder preguntas en lenguaje natural y crear
estrategias de marketing inteligentes.

💡 Actualmente las páginas **1 (Dashboard)** y **2 (Gestión de Citas)**
consumen directamente los datos desde la **API Central (`pi_movil2`)**,  
mientras que el módulo de IA opera de forma independiente usando servicios
de **Google Generative AI (Gemini)**.

======================================================================
                       🚀 INFORMACIÓN DE DESPLIEGUE
======================================================================

🌐 Plataforma: Streamlit Cloud (https://streamlit.io/cloud)  
🔗 URL Pública: https://kingdombarberdashboard.streamlit.app  
🧩 API Consumida: https://pi-movil2-0.onrender.com  
📦 Estado: Activo y en Producción  

======================================================================
                  🧭 GUÍA DE EJECUCIÓN Y MANUAL DE USO
======================================================================

1️⃣ REQUISITOS PREVIOS  
----------------------
- 🐍 Python 3.9 o superior  
- 📦 pip (gestor de paquetes)  

⚠️ Nota:  
La aplicación es un cliente de datos.  
Debe conectarse a la API de Java (`pi_movil2`) para obtener información real.  
Por defecto se conecta al entorno de producción.

2️⃣ INSTALACIÓN Y EJECUCIÓN  
----------------------------
# Crear entorno virtual
python -m venv .venv

# Activar entorno (Windows)
.venv\Scripts\activate

# Activar entorno (macOS / Linux)
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
streamlit run inicio.py

La app se abrirá automáticamente en el navegador.

🔐 Nota sobre IA:  
Para el módulo del Asistente de IA, es necesario un archivo
`.streamlit/secrets.toml` con tu clave:
GOOGLE_API_KEY = "tu_clave_aqui"

======================================================================
                          💡 RESUMEN DEL PROYECTO
======================================================================

El **Panel de Gestión y Análisis (PI_NTP)** funciona como el cerebro visual
del ecosistema Kingdom Barber, diseñado para el análisis de datos y la
toma de decisiones estratégicas.  

Toda la información se consume en tiempo real desde la **API Central**
(`pi_movil2`), mientras que la IA utiliza **Google Gemini** para análisis
avanzado, generación de reportes automáticos y asesoramiento de marketing.  

Además, se ha incorporado una **nueva cuarta página** dedicada al análisis
de **datasets públicos** de datos.gov.co, permitiendo comparar la barbería
con el mercado nacional y regional.

======================================================================
                        🎯 OBJETIVOS DEL PROYECTO
======================================================================

✅ Visualizar KPIs Clave: Ofrecer un dashboard dinámico con los indicadores
más importantes del negocio.  

✅ Facilitar la Consulta: Permitir búsquedas y filtros detallados sobre el
historial completo de citas.  

✅ Integrar IA: Incluir un asistente inteligente (Gemini) que genere reportes,
responda preguntas y proponga estrategias de marketing.  

✅ Analizar el Mercado: Incorporar un módulo que use datasets reales para
evaluar el contexto competitivo de las barberías en Colombia.

======================================================================
                           🧠 STACK TECNOLÓGICO
======================================================================

🐍 Lenguaje: Python  
🧱 Framework Web: Streamlit  
📊 Procesamiento: Pandas  
📈 Visualización: Plotly Express  
📄 Reportes PDF: FPDF2  
🤖 Inteligencia Artificial: Google Generative AI (Gemini)  
🌐 Consumo de API: requests  
🗄️ Back-End Consumido: Java + Spring Boot (pi_movil2)  

======================================================================
                🗂️ ARQUITECTURA Y ESTRUCTURA DE CARPETAS
======================================================================

El proyecto adopta una **arquitectura modular**, donde cada página de Streamlit
se ejecuta como un script independiente dentro de `pages/`.

📂 pi_ntp/
│
├── 📂 .streamlit/
│   └── 📜 secrets.toml          → Claves de API (ej. Google Gemini)
│
├── 📂 assets/                   → Recursos estáticos (logos, imágenes)
│
├── 📂 pages/                    → Secciones principales de la aplicación
│   ├── 1_Dashboard.py           → Dashboard general de KPIs
│   ├── 2_Gestion_de_Citas.py    → Exploración y control de citas
│   ├── 3_Asistente_IA.py        → Asistente inteligente (Gemini)
│   └── 4_Datasets_Reales.py     → Análisis de datasets públicos
│
├── 📜 inicio.py                 → Página de inicio y punto de entrada
├── 📜 data_manager.py           → Conexión y manejo de datos desde la API
├── 📜 report_generator.py       → Lógica para generar reportes PDF
└── 📜 requirements.txt          → Lista de dependencias de Python  

======================================================================
                   🔄 FLUJO DE DATOS Y DESPLIEGUE
======================================================================

🧭 Flujo Típico: Carga del Dashboard  

1️⃣ Usuario (Streamlit)  
Selecciona filtros o visualiza la página del dashboard.  

2️⃣ Front-End (1_Dashboard.py)  
Llama a funciones del módulo `data_manager.py` para obtener los datos.  

3️⃣ Lógica de Datos (`data_manager.py`)  
Realiza peticiones `GET` a la API (`pi_movil2`), recibe los JSON y los
transforma en DataFrames de Pandas para análisis.  

4️⃣ Visualización  
Los gráficos son generados con **Plotly Express**, de forma dinámica
y totalmente interactiva.  

5️⃣ Asistente IA (`3_Asistente_IA.py`)  
Utiliza **Google Gemini** para análisis textual, generación de reportes y
respuestas automáticas en lenguaje natural.  

6️⃣ Nuevo Módulo (`4_Datasets_Reales.py`)  
Analiza datasets de datos.gov.co, genera dashboards comparativos y
conclusiones dinámicas basadas en filtros seleccionados.  

======================================================================
                   ☁️ DESPLIEGUE Y AUTOMATIZACIÓN (CLOUD)
======================================================================

🚀 Plataforma: Streamlit Cloud  
🔄 CI/CD: Integrado con GitHub (despliegue automático al hacer push a main)  
🔐 Gestión de Secrets: Claves y tokens seguros mediante `.streamlit/secrets.toml`  
📦 Dependencias: Instaladas automáticamente desde `requirements.txt`  
🌍 Producción: Acceso público desde  
👉 https://kingdombarberdashboard.streamlit.app  

======================================================================
                    👥 AUTORES Y CONTRIBUIDORES
======================================================================

👤 Juan Manuel Rivera  
👤 Andrés Vallejo  
👤 Alejandro Urrego  

Repositorio oficial:  
🔗 https://github.com/JuanRivera24/pi_ntp2.0  

======================================================================
                           ✨ FIN DEL DOCUMENTO
======================================================================

