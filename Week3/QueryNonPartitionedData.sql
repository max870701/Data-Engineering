-- Query from non partitioned data
-- This query will process 12.82 MB when run.
SELECT DISTINCT PULocationID
FROM `amazing-modem-411901.nyctaxi.green_tripdata_non_partitioned`
WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'
