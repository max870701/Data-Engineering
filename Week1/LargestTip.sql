WITH drop_tip AS (
     SELECT "DOLocationID", tip_amount
     FROM green_taxi_data
     WHERE "PULocationID" = (
         SELECT DISTINCT "LocationID"
         FROM taxi_zone_data
         WHERE "Zone" = 'Astoria'
     )
     AND (lpep_pickup_datetime BETWEEN '2019-09-01 00:00:00' AND '2019-09-30 23:59:59')
 )
 
SELECT t."Zone", MAX(d.tip_amount) AS "max_tip"
FROM drop_tip AS d
INNER JOIN taxi_zone_data AS t
ON d."DOLocationID" = t."LocationID"
WHERE t."Zone" = 'Central Park' OR t."Zone" = 'Jamaica'
OR t."Zone" = 'JFK Airport' OR t."Zone" = 'Long Island City/Queens Plaza'
GROUP BY t."Zone"
ORDER BY MAX(d.tip_amount) DESC;