SELECT t."Borough", SUM(total_amount) AS "Total Amount"
FROM green_taxi_data AS g
INNER JOIN taxi_zone_data AS t
ON g."PULocationID" = t."LocationID"
WHERE t."Borough" IS NOT NULL
AND (lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59')
GROUP BY t."Borough"
ORDER BY SUM(total_amount) DESC;