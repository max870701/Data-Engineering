variable "credentials" {
  description = "Credentials Path"
  default     = "../mage-zoomcamp/amazing-modem-411901-e2331808b339.json"
}

variable "project" {
  description = "Project Name"
  default     = "amazing-modem-411901"
}

variable "region" {
  description = "Project Region"
  default     = "us-west1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "Name of the BigQuery Dataset"
  default     = "mage_zoomcap"
}

variable "gcs_bucket_name" {
  description = "Google Cloud Storage Bucket Name"
  default     = "amazing-modem-411901-mage-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}