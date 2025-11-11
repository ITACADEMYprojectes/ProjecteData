# Sanity check 10/11/2025
# Total registros:
SELECT COUNT(apartment_id) AS conteo
FROM Tourist_Accommodation10112025;


#ID únicos:
SELECT COUNT(DISTINCT apartment_id) AS conteo_unicos 
FROM Tourist_Accommodation10112025;


# ID Extras:
# Al resultado le resto el numero de filas de apartment_id duplicados

SELECT COUNT(apartment_id) - COUNT(DISTINCT apartment_id) AS conteo_extras
FROM Tourist_Accommodation10112025;


# ID Duplicados exactos:
SELECT 
apartment_id,
name,
description,
host_id,
neighbourhood_name,
neighbourhood_district,
room_type,
accommodates,
bathrooms,
bedrooms,
beds,
amenities_list,
price,
minimum_nights,
maximum_nights,
has_availability,
availability_30,
availability_60,
availability_90,
availability_365,
number_of_reviews,
first_review_date,
last_review_date,
review_scores_rating,
review_scores_accuracy,
review_scores_cleanliness,
review_scores_checkin,
review_scores_communication,
review_scores_location,
review_scores_value,
is_instant_bookable,
reviews_per_month,
country,
city,
insert_date,
COUNT(*) AS total_duplicados
FROM
    Tourist_Accommodation10112025
GROUP BY
    apartment_id,
name,
description,
host_id,
neighbourhood_name,
neighbourhood_district,
room_type,
accommodates,
bathrooms,
bedrooms,
beds,
amenities_list,
price,
minimum_nights,
maximum_nights,
has_availability,
availability_30,
availability_60,
availability_90,
availability_365,
number_of_reviews,
first_review_date,
last_review_date,
review_scores_rating,
review_scores_accuracy,
review_scores_cleanliness,
review_scores_checkin,
review_scores_communication,
review_scores_location,
review_scores_value,
is_instant_bookable,
reviews_per_month,
country,
city,
insert_date
HAVING
    COUNT(*) > 1;

