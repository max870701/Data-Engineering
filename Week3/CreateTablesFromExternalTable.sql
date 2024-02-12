-- Create a non partitioned table from external table
CREATE OR REPLACE TABLE `amazing-modem-411901.nyctaxi.green_tripdata_non_partitioned` AS
SELECT
  *
FROM
  `amazing-modem-411901.nyctaxi.external_green_tripdata`;

-- Create a partitioned table by lpep_pickup_datetime from external table
CREATE OR REPLACE TABLE `amazing-modem-411901.nyctaxi.green_tripdata_partitioned`
PARTITION BY
  DATE(lpep_pickup_datetime)
AS
SELECT
  *
FROM
  `amazing-modem-411901.nyctaxi.external_green_tripdata`;