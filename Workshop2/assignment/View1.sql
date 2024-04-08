CREATE MATERIALIZED VIEW avg_time_between_zones AS (
    WITH t AS (
        SELECT
            trip_data.pulocationid,
            trip_data.dolocationid,
            EXTRACT(EPOCH FROM (trip_data.tpep_dropoff_datetime - trip_data.tpep_pickup_datetime)) / 3600 AS trip_time_hours
        FROM trip_data
        WHERE trip_data.tpep_dropoff_datetime >= trip_data.tpep_pickup_datetime
    )
    SELECT
        pickup_zone.zone AS "Pickup Zone",
        dropoff_zone.zone AS "Dropoff Zone",
        ROUND(AVG(trip_time_hours), 2) AS "Average Trip Time (Hours)",
        ROUND(MAX(trip_time_hours), 2) AS "Maximum Trip Time (Hours)",
        ROUND(MIN(trip_time_hours), 2) AS "Minimum Trip Time (Hours)"
    FROM t
    JOIN taxi_zone AS pickup_zone ON t.pulocationid = pickup_zone.location_id
    JOIN taxi_zone AS dropoff_zone ON t.dolocationid = dropoff_zone.location_id
    GROUP BY 1, 2
);
-- DROP MATERIALIZED VIEW IF EXISTS avg_time_between_zones;
-- trip_data.pulocationid
-- trip_data.dolocationid
-- trip_data.tpep_pickup_datetime
-- trip_data.tpep_dropoff_datetime
-- taxi_zone.location_id
-- taxi_zone.zone