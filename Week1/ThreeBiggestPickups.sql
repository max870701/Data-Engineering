SELECT z."Borough", ROUND(CAST(SUM(g.total_amount) AS numeric), 2) as "Total Amount"
FROM green_taxi_data AS g
INNER JOIN taxi_zone_data AS z
ON g."PULocationID" = z."LocationID"
WHERE g.lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59'
GROUP BY z."Borough"
ORDER BY "Total Amount" DESC;