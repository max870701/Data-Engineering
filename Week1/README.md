# Homework 1
## Question 1. Docker tags
```bash
--rm
```
## Question 2. Docker run: version of wheel
```bash
0.42.0
```
## Question 3. Count records
```sql
SELECT COUNT(*)
FROM green_taxi_data
WHERE (lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59')
AND (lpep_dropoff_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59');
```
## Question 4. Largest trip for each day
```sql
SELECT t."Borough", SUM(total_amount) AS "Total Amount"
FROM green_taxi_data AS g
INNER JOIN taxi_zone_data AS t
ON g."PULocationID" = t."LocationID"
WHERE t."Borough" IS NOT NULL
AND (lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59')
GROUP BY t."Borough"
ORDER BY SUM(total_amount) DESC;
```
## Question 5. Three biggest pickups
```sql
SELECT z."Borough", ROUND(CAST(SUM(g.total_amount) AS numeric), 2) as "Total Amount"
FROM green_taxi_data AS g
INNER JOIN taxi_zone_data AS z
ON g."PULocationID" = z."LocationID"
WHERE g.lpep_pickup_datetime BETWEEN '2019-09-18 00:00:00' AND '2019-09-18 23:59:59'
GROUP BY z."Borough"
ORDER BY "Total Amount" DESC;
```
## Question 6. Largest tip
```sql
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
```
## Question 7. Terraform
```bash
terraform apply
```
```bash
Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_bigquery_dataset.dataset will be created
  + resource "google_bigquery_dataset" "dataset" {
      + creation_time              = (known after apply)
      + dataset_id                 = "demo_dataset"
      + default_collation          = (known after apply)
      + delete_contents_on_destroy = false
      + effective_labels           = (known after apply)
      + etag                       = (known after apply)
      + id                         = (known after apply)
      + is_case_insensitive        = (known after apply)
      + last_modified_time         = (known after apply)
      + location                   = "US"
      + max_time_travel_hours      = (known after apply)
      + project                    = "amazing-modem-411901"
      + self_link                  = (known after apply)
      + storage_billing_model      = (known after apply)
      + terraform_labels           = (known after apply)
    }

  # google_storage_bucket.bucket will be created
  + resource "google_storage_bucket" "bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "amazing-modem-411901-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + rpo                         = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 2 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_bigquery_dataset.dataset: Creating...
google_storage_bucket.bucket: Creating...
google_bigquery_dataset.dataset: Creation complete after 1s [id=projects/amazing-modem-411901/datasets/demo_dataset]
google_storage_bucket.bucket: Creation complete after 2s [id=amazing-modem-411901-terra-bucket]

Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
```