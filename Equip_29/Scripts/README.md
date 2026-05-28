# Scripts Carpeta para almacenar los scripts
## 1. Contexto del negocio

El dataset describe alojamientos turísticos ofertados para alquiler.
“El conjunto de datos contiene información detallada sobre alojamientos turísticos ofertados para alquiler a corto plazo. Incluye características del alojamiento, ubicación, precios, disponibilidad y valoraciones de los usuarios.”
Con esto, parece que el objetivo del negocio está relacionado con:
•	Gestión de oferta turística (plataformas tipo Airbnb, Booking, etc.)
•	Optimización de precios y ocupación
•	Análisis de competencia por barrio/distrito
•	Mejora de la experiencia del huésped
•	Detección de patrones de demanda y estacionalidad
Nos permite estudiar tanto **aspectos operativos** (disponibilidad, noches mínimas, capacidad) como **aspectos de mercado** (precio, ubicación, valoraciones).

IMPORTANTE: De la variable “insert_date” entendemos que el data set va a ser una foto o captura estática de ese momento y por el resto de variables, no podremos hacer un estudio histórico dinámico y solo estudios de lo que hay en ese instante de la foto, tanto valoraciones totales como disponibilidad a futuro. Esto hará que sea muy importante la temporalidad con la que se saca esta foto sobre todo para predecir demandas.

## 2.	Revisión de Características y Alcance del Dataset
Las variables se pueden distribuir en 6 grupos:
    **a. Identificación y descripción**
    i.	Variables orientadas a la auditoría de activos y al análisis del perfil del oferente. Permiten distinguir entre la profesionalización del sector y el alquiler de particulares.
    ii.	Variables: "apartment_id", "name", "description", "host_id".
    iii.	Nos permiten:
        1.	Identificar cada anuncio.
        2.	Analizar propietarios con múltiples alojamientos.
        3.	Estudiar la calidad del texto descriptivo.

    **b. Ubicación geográfica**
    i.	Variables: neighbourhood_name, neighbourhood_district, city, country.
    ii.	Nos permiten:
        1.	Zonas con mayor oferta
        2.	Relación entre precio y ubicación
        3.	Detección de “hotspots” turísticos

    **c. Características físicas del alojamiento**
    i.	Características técnicas que definen el producto y su capacidad, fundamentales para la normalización y comparación de precios
    ii.	Variables: room_type, accommodates, bathrooms, bedrooms, beds, amenities_list
    iii.	Nos permiten:
        1.	Clasificar tipos de alojamiento
        2.	Estudiar qué características influyen en el precio
        3.	Analizar la calidad del inventario
    **d. Precio y reglas de reserva**
    i.	Variables: price, minimum_nights, maximum_nights, is_instant_bookable.
    ii.	Nos permiten:
        1.	Modelos y estrategias de pricing
        2.	Identificar restricciones de estancia
        3.	Analizar fricción en la reserva

    **d.	Precio y reglas de reserva**
    i.	Variables: price, minimum_nights, maximum_nights, is_instant_bookable.
    ii.	Nos permiten:
        1.	Modelos y estrategias de pricing
        2.	Identificar restricciones de estancia
        3.	Analizar fricción en la reserva
    
    **e.	Disponibilidad y Ocupación**
    i.	Indicadores de inventario que permiten inferir el comportamiento de la demanda y la presión del mercado en diferentes horizontes temporales
    ii.	Variables: has_availability, availability_30, availability_60, availability_90, availability_365.
    iii.	Nos permiten:
        1.	Estudiar ocupación estimada
        2.	Detectar estacionalidad
        3.	Identificar alojamientos con baja rotación

    **f.	Reseñas y puntuaciones**
    i.	Métricas de rendimiento cualitativo. Es crítico notar que el review_scores_rating utiliza una escala de 0 a 100, mientras que el resto de las subpuntuaciones operan en una escala de 0 a 10
    ii.	Variables: 
    review_scores_rating, review_scores_accuracy, review_scores_cleanliness, review_scores_checkin, review_scores_communication, review_scores_location, review_scores_value.
    iii.	Nos permite:
        1.	Medir reputación
        2.	Analizar calidad percibida
        3.	Relacionar puntuaciones con precio y ocupación

    **g.	Actividad y metadatos temporales**
    i.	Variables que muestran la actividad del anuncio a lo largo del tiempo y el momento de extracción de datos. Es clave para aproximar la demanda y contextualizar temporalmente el análisis.
    ii.	Variables:
    number of reviews, reviews_per_month, first_review_date, last_review_date, insert_date.
    iii.	Permite:
        1.	Aproximar la popularidad y la demanda mediante el volumen( number_of_reviews) y la frecuencia (reviews_per_month) de las reseñas.
        2.	Conocer la antigüedad del anuncio y su actividad más reciente, un last_review_date muy antiguo sugiere un alojamiento inactivo.
        3.	Situar temporalmente la “foto del dataset (insert_date) y normalizar las métricas de reputación para mitigar el sesgo de madurez de las reseñas.

## 3.	Identificación de posibles limitaciones
    a.	Datos estáticos. La variable insert_date indica que es una foto en el tiempo, no una serie temporal completa.
    b.	Disponibilidad ≠ ocupación real. Las variables availability_x indican días disponibles, pero no reservas reales y no distingue entre una reserva real y un bloqueo deliberado del calendario por parte del host (ej. mantenimiento o uso personal).
    c.	Posibles valores faltantes. No siempre se rellenan las encuestas de satisfacción y eso puede sesgar las medidas hacia arriba o hacia abajo ocultando la verdadera calidad.
    d.	Sesgo de madurez. de Reseñas. Los alojamientos nuevos tienen un volumen de reseñas por lo que se requiere normalizar el rating utilizando por ejemplo reviews_per_month para evitar que anuncios recientes distorsionen el ranking de "Top Rated".
    e.	Precio sin desglose. No indica, por ejemplo, si incluye limpieza, si es por noche o por estancia ni si hay tarifas dinámicas.

## 4.	Areas de interés inicial
    a.	Relación entre precio y características: Capacidad, nº habitaciones, tipo de alojamiento, barrio/distrito, amenities, etc.
    b.	Análisis de Presión de Demanda: 
        i.	Alojamientos con alta disponibilidad → baja demanda
        ii.	Alojamientos con baja disponibilidad → oportunidad de subir precios
    c.	Determinantes de la Calidad Percibida: Utilizar las subpuntuaciones para entender qué factor (limpieza, ubicación, etc.) tiene mayor correlación con el review_scores_rating
    d.	Segmentación de la Profesionalización del Host: Clasificar a los oferentes según la frecuencia de su host_id. Tip del consultor: Diferenciar entre "Professional Hosts" (gestores de flotas) y "Peer-to-Peer Hosts" puede ser vital para entender la estabilidad y agresividad de precios en una zona.
    e.	Análisis geoespacial: Mapeo de clusters de rentabilidad, mapas de calor de precios, mapas de disponibilidad, mapas de valoración, etc.


