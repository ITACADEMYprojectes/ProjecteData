
# Queries para responder a las preguntas iniciales

SELECT *
FROM Tourist_Accommodation;

SELECT Count(apartment_id)
FROM Tourist_Accommodation;

SELECT Count(apartment_id), apartment_id
FROM Tourist_Accommodation
group by apartment_id
Having Count(apartment_id) > 1;

# Queries para responder las preguntas iniciales con la base de datos límpia

SELECT *
FROM Tourist_Accommodation_Clean;

SELECT Count(apartment_id)
FROM Tourist_Accommodation_Clean;

SELECT Count(apartment_id), apartment_id
FROM Tourist_Accommodation_Clean
group by apartment_id
Having Count(apartment_id) > 1;




