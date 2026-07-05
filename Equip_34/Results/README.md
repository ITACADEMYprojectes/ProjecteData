# Results Carpeta para almacenar resultados y salidas del proyecto.# Carpeta Results

Esta carpeta contiene los entregables finales del Sprint 1 del proyecto **StaySpain**.

Los archivos almacenados aquí representan la capa final de comunicación del análisis: el dashboard de indicadores clave y la presentación final de resultados para la toma de decisiones de negocio.

---

## Archivos incluidos

### `KPIs.pbix`

Archivo de Power BI que contiene el dashboard de indicadores clave del proyecto.

Los principales KPI calculados son:

- **Tasa de ocupación mensual:** 59,03%
- **Ciudad con mayor ocupación:** Madrid, con 65,3%
- **Índice de satisfacción general:** 9,20 sobre 10
- **Ítem con mayor satisfacción:** Comunicación, con 96,43 sobre 100

El dashboard permite resumir el rendimiento general del negocio desde las perspectivas de ocupación y experiencia del cliente.

---

### `Data Analytics Presentation.pdf`

Presentación final del Sprint 1.

Resume los principales resultados de las tres áreas de negocio:

- Marketing y Estrategia Comercial;
- Operaciones y Gestión de Inventario;
- Experiencia del Cliente;
- conclusiones y propuestas de negocio.

La presentación incluye visualizaciones, conclusiones y recomendaciones basadas en los análisis realizados por el equipo.

---

## Resultados principales

### Marketing y Estrategia Comercial

El análisis muestra que el precio depende principalmente de:

- la ciudad;
- el tipo de alojamiento;
- la combinación entre ubicación y categoría.

Los destinos insulares presentan precios superiores, mientras que las habitaciones privadas y compartidas se sitúan en los segmentos de menor coste.

La recomendación principal es aplicar una estrategia de precios diferenciada por ciudad y tipo de alojamiento.

### Operaciones y Gestión de Inventario

Madrid y Barcelona presentan los niveles de disponibilidad más bajos, mientras que Mallorca y Menorca muestran un mayor margen de disponibilidad.

Estos resultados pueden indicar:

- mayor demanda u ocupación en Madrid y Barcelona;
- mayor margen para optimizar la ocupación en las islas;
- necesidad de adaptar la estrategia operativa según la ciudad.

### Experiencia del Cliente

La satisfacción general es alta:

- media global de 92 sobre 100;
- 89,67% de los alojamientos evaluados supera 80 puntos;
- Sevilla presenta los mejores resultados;
- Barcelona mantiene una puntuación alta, aunque es la más baja del conjunto.

La comunicación y el check-in son las principales fortalezas, mientras que la limpieza representa la oportunidad de mejora más clara.

También se recomienda aumentar la captación de reseñas en las ciudades con menor cobertura.

---

## Propuestas de negocio

A partir de los resultados obtenidos, el equipo propone:

- aplicar una estrategia de precios segmentada por ciudad y tipo de alojamiento;
- optimizar la ocupación en los destinos con mayor disponibilidad;
- reforzar los estándares de limpieza;
- mantener la calidad en comunicación y check-in;
- aumentar la captación de reseñas en ciudades con menor cobertura;
- utilizar los KPI como herramienta de seguimiento del rendimiento.

---

## Relación con el resto del proyecto

Los resultados de esta carpeta se generan a partir del dataset final:

`Data/clean_dataset_29_06_2026.csv`

y de los notebooks almacenados en:

`Scripts/`

El flujo completo del proyecto es:

```text
Data Understanding
→ EDA
→ Data Cleaning
→ Data Transformation
→ Data Reduction
→ Análisis departamental
→ KPI
→ Presentación de resultados
