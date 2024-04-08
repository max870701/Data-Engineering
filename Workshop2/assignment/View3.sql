CREATE MATERIALIZED VIEW zones_pickup_count AS (
    WITH latest_time AS (
        SELECT
            MAX(tpep_pickup_datetime) AS latest_pickup_time,
            MAX(tpep_pickup_datetime) - INTERVAL '17' hour AS start_pickup_time 
        FROM trip_data
        WHERE tpep_dropoff_datetime >= tpep_pickup_datetime
    )

    SELECT
        pickup_zone.zone AS "Pickup Zone",
        COUNT(pickup_zone.location_id) AS "Pickup Times"
    FROM trip_data AS t
    JOIN taxi_zone AS pickup_zone ON t.pulocationid = pickup_zone.location_id
    JOIN taxi_zone AS dropoff_zone ON t.dolocationid = dropoff_zone.location_id
    WHERE t.tpep_pickup_datetime BETWEEN '2022-01-02 17:53:33' AND '2022-01-03 10:53:33'
    GROUP BY 1
);