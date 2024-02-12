-- Query from partitioned data
-- This query will process 1.12 MB when run
SELECT DISTINCT PULocationID
FROM `amazing-modem-411901.nyctaxi.green_tripdata_partitioned`
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'