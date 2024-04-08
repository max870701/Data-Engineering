CREATE MATERIALIZED VIEW zones_pickup_count AS (
    WITH latest_time AS (
        SELECT
            MAX(tpep_pickup_datetime) AS latest_pickup_time,
            MAX(tpep_pickup_datetime) - INTERVAL '17' hour AS start_pickup_time 
        FROM trip_data
    )

    SELECT
        pickup_zone.zone AS "Pickup Zone",
        COUNT(pickup_zone.location_id) AS "Pickup Times"
    FROM trip_data AS t
    JOIN taxi_zone AS pickup_zone ON t.pulocationid = pickup_zone.location_id
    JOIN taxi_zone AS dropoff_zone ON t.dolocationid = dropoff_zone.location_id
    JOIN latest_time ON TRUE
    WHERE t.tpep_pickup_datetime BETWEEN latest_time.start_pickup_time AND latest_time.latest_pickup_time
    GROUP BY 1
);