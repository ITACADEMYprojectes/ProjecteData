USE Equip_26;

-- TOTAL REGISTROS
SELECT COUNT(*)
FROM `Tourist_Accommodation`;

-- TOTAL ID UNICOS
SELECT COUNT(DISTINCT apartment_id)
FROM `Tourist_Accommodation`;

-- TOTAL ID EXTRA
SELECT COUNT(*) - COUNT(DISTINCT apartment_id)
FROM `Tourist_Accommodation`;

-- TOTAL DUPLICADOS EXACTOS
SELECT `Tourist_Accommodation`.`apartment_id`,
    `Tourist_Accommodation`.`name`,
    `Tourist_Accommodation`.`description`,
    `Tourist_Accommodation`.`host_id`,
    `Tourist_Accommodation`.`neighbourhood_name`,
    `Tourist_Accommodation`.`neighbourhood_district`,
    `Tourist_Accommodation`.`room_type`,
    `Tourist_Accommodation`.`accommodates`,
    `Tourist_Accommodation`.`bathrooms`,
    `Tourist_Accommodation`.`bedrooms`,
    `Tourist_Accommodation`.`beds`,
    `Tourist_Accommodation`.`amenities_list`,
    `Tourist_Accommodation`.`price`,
    `Tourist_Accommodation`.`minimum_nights`,
    `Tourist_Accommodation`.`maximum_nights`,
    `Tourist_Accommodation`.`has_availability`,
    `Tourist_Accommodation`.`availability_30`,
    `Tourist_Accommodation`.`availability_60`,
    `Tourist_Accommodation`.`availability_90`,
    `Tourist_Accommodation`.`availability_365`,
    `Tourist_Accommodation`.`number_of_reviews`,
    `Tourist_Accommodation`.`first_review_date`,
    `Tourist_Accommodation`.`last_review_date`,
    `Tourist_Accommodation`.`review_scores_rating`,
    `Tourist_Accommodation`.`review_scores_accuracy`,
    `Tourist_Accommodation`.`review_scores_cleanliness`,
    `Tourist_Accommodation`.`review_scores_checkin`,
    `Tourist_Accommodation`.`review_scores_communication`,
    `Tourist_Accommodation`.`review_scores_location`,
    `Tourist_Accommodation`.`review_scores_value`,
    `Tourist_Accommodation`.`is_instant_bookable`,
    `Tourist_Accommodation`.`reviews_per_month`,
    `Tourist_Accommodation`.`country`,
    `Tourist_Accommodation`.`city`,
    `Tourist_Accommodation`.`insert_date`,
    COUNT(*) AS ctn
FROM `Equip_26`.`Tourist_Accommodation`
GROUP BY `apartment_id`,
    `name`,
    `description`,
    `host_id`,
    `neighbourhood_name`,
    `neighbourhood_district`,
    `room_type`,
    `accommodates`,
    `bathrooms`,
    `bedrooms`,
    `beds`,
    `amenities_list`,
    `price`,
    `minimum_nights`,
    `maximum_nights`,
    `has_availability`,
    `availability_30`,
    `availability_60`,
    `availability_90`,
    `availability_365`,
    `number_of_reviews`,
    `first_review_date`,
    `last_review_date`,
    `review_scores_rating`,
    `review_scores_accuracy`,
    `review_scores_cleanliness`,
    `review_scores_checkin`,
    `review_scores_communication`,
    `review_scores_location`,
    `review_scores_value`,
    `is_instant_bookable`,
    `reviews_per_month`,
    `country`,
    `city`,
    `insert_date`
HAVING count(*)>1

