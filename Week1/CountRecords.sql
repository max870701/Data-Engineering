SELECT COUNT(*)
FROM green_taxi_data
WHERE (lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59')
AND (lpep_dropoff_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59');