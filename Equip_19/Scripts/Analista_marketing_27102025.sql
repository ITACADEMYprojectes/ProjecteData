# Quin és el preu mitjà dels allotjaments per tipus d'allotjament a cada ciutat?
SELECT ROUND(AVG(price),2) AS Average, room_type, city
FROM Tourist_Accommodation_Clean
GROUP BY room_type, city
ORDER BY city;