============================================================
  MANUAL DE USUARIO - SISTEMA DE GESTIÓN KINGDOM BARBER
============================================================

Bienvenido al sistema de análisis y gestión de Kingdom Barber.
Este documento explica cómo utilizar las dos secciones principales de la aplicación:
el Dashboard General y la Gestión de Citas.


---------------------------------
-- 1. Dashboard General (📊) --
---------------------------------

Esta pantalla ofrece una vista global y visual del rendimiento del negocio.
Permite analizar tendencias y resultados clave de forma rápida.

Funcionalidades Principales:

a) Filtrado Avanzado:
   En la barra lateral izquierda encontrarás un panel de filtros que se aplican a todo el dashboard. Los filtros funcionan en cascada, de más general a más específico:

   - Sede: Permite ver los datos de una sede en particular o de "Todas" en conjunto.
   - Barbero: Muestra los barberos disponibles según la sede seleccionada. Puedes analizar a un barbero específico o a "Todos".
   - Cliente: Permite enfocarse en la actividad de un cliente en particular.

b) Métricas Clave:
   En la parte superior, verás 4 indicadores que resumen el estado actual según los filtros aplicados:

   - Ingresos Totales: Suma total del dinero generado por las citas.
   - Citas Registradas: Conteo total de citas.
   - Servicio Popular: El servicio más demandado.
   - Barbero Top (Ingresos): El barbero que más ingresos ha generado.

c) Gráficos y Análisis Visual:
   El dashboard contiene cuatro gráficos interactivos:

   - Distribución de Ingresos por Servicio: Un gráfico circular que muestra qué porcentaje de los ingresos totales aporta cada servicio. Ideal para saber qué servicios son los más rentables.
   - Carga de Trabajo por Barbero: Un gráfico de barras que compara el número de citas atendidas por cada barbero. Útil para balancear el trabajo.
   - Ingresos Generados por Barbero: Un gráfico de barras que muestra cuánto dinero ha generado cada barbero. Complementa al de carga de trabajo.
   - Evolución de Citas en el Tiempo: Un gráfico de líneas que muestra la cantidad de citas a lo largo del tiempo. Puedes cambiar la vista a "Día", "Semana" o "Mes" para identificar patrones y tendencias. Incluye una línea de promedio para comparar el rendimiento.


d) Inventario de Productos:
   Al final de la página se muestra una tabla con el inventario de productos, cargado en tiempo real desde una API externa.


----------------------------------------
-- 2. Gestión de Citas (🗓️) --
----------------------------------------

Esta sección es la herramienta operativa para buscar, revisar y gestionar el detalle de todas las citas registradas en el sistema.

Funcionalidades Principales:

a) Búsqueda y Filtrado Detallado:
   La barra lateral permite combinar múltiples filtros para encontrar citas específicas:

   - Filtrar por Sede: Muestra solo las citas de la ubicación seleccionada.
   - Filtrar por Barbero: Acota la búsqueda a un barbero en particular.
   - Filtrar por Cliente: Muestra el historial de citas de un solo cliente.
   - Filtrar por Rango de Fecha: Permite seleccionar un periodo de tiempo (inicio y fin) para ver las citas dentro de esas fechas.

b) Tabla de Resultados:
   La tabla principal muestra todas las citas que coinciden con los filtros seleccionados, ordenada por fecha (de la más reciente a la más antigua). Incluye columnas clave como:

   - Fecha y Hora de la cita.
   - Sede, Cliente y Barbero asignados.
   - Servicio realizado y su Precio.

c) Métrica de Ingresos:
   Sobre la tabla se muestra un indicador con la suma de los ingresos correspondientes únicamente a las citas que se están visualizando en la tabla filtrada.

```