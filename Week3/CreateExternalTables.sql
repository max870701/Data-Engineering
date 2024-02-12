-- Creating External Table Referring to GCS Path
CREATE OR REPLACE EXTERNAL TABLE `amazing-modem-411901.nyctaxi.external_green_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://amazing-modem-411901-mage-bucket/green_tripdata_2022-*.parquet'
  ]
);