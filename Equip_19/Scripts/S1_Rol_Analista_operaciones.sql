# Pregunta de negocio para el rol de Analista de operaciones y gestión de inventario: 
# Cuál es la disponibilidad media de los alojamientos turísticos en los diferentes términos (30, 60, 90 y 365 días) en cada ciudad?
# Previo al cálculo (en la subconsulta), se seleccionan los datos sin apartment_id dulpicados, 
# quedándonos con la fecha más reciente de publicacion del anuncio.

select city, 
round(avg(availability_30),2) as "AVG_30days" , 
round(avg(availability_60),2) as "AVG_60days", 
round(avg(availability_90),2) as "AVG_90days", 
round(avg(availability_365),2) as "AVG_365days"
FROM Tourist_Accommodation t1
INNER JOIN ( SELECT apartment_id,
            MAX(insert_date) AS max_insert_date
            FROM Tourist_Accommodation
            GROUP BY apartment_id
            ) AS t2
ON t1.apartment_id = t2.apartment_id
AND t1.insert_date = t2.max_insert_date
group by city
;