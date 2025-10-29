# Puntuación media dada a los alojamientos por los usuarios
SELECT ROUND(avg(review_scores_rating),2)
FROM Tourist_Accommodation;

# Porcentaje de alojamientos con nota general superior a 80 en cada ciudad
SELECT city,   ROUND(
        COUNT(CASE WHEN review_scores_rating > 80 THEN 1 END) * 100.0 / COUNT(*),
        2
    ) AS pt_sup_80
FROM 
    Tourist_Accommodation
GROUP BY 
    city
ORDER BY pt_sup_80 DESC;