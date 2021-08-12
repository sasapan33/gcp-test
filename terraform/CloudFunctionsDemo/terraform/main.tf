provider "google" { 
  credentials = file(var.gcp_credentials)
  project = var.gcp_project
  region = var.gcp_region
}

resource "google_storage_bucket" "bucket" {
  name = "SOURCECODE_BUCKET" # sourcecode會先打包後放入這個bucket中
}

############
data "archive_file" "src" { # 打包sourcecode
  type        = "zip"
  source_dir  = "${path.root}/../src" # Directory where your Python source code is
  output_path = "${path.root}/../generated/src.zip"
}

resource "google_storage_bucket_object" "archive" { #放入GCS bucket
  name   = "${data.archive_file.src.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = "${path.root}/../generated/src.zip"
}

resource "google_cloudfunctions_function" "sasa_http_sample" { # deploy cloud functions: function name: `sasa_http_sample`
  name                  = "sasa_http_sample" # mapping main.py function name
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive.name
  service_account_email = "YOUR_SERVICE_ACCOUNT" #optional 沒有就用default的
  runtime               = "python37"
  trigger_http          = true # if https, set true. 跟`event_trigger`不能一起用
  timeout               = 60
  environment_variables = { # 注入環境變數
    PROJECT_ID = var.gcp_project # terraform裡面的變數
    DIST_BUCKET = "BUCKET1"
    SRC_BUCKET = "BUCKET2"
  }
}

resource "google_cloudfunctions_function_iam_member" "invoker" { # 宣告invoker(誰可以執行這隻cloud functions)
  project        = google_cloudfunctions_function.sasa_http_sample.project
  region         = google_cloudfunctions_function.sasa_http_sample.region
  cloud_function = google_cloudfunctions_function.sasa_http_sample.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

############## 
data "archive_file" "src2" {
  type        = "zip"
  source_dir  = "${path.root}/../src2" # Directory where your Python source code is
  output_path = "${path.root}/../generated/src2.zip"
}

resource "google_storage_bucket_object" "archive2" {
  name   = "${data.archive_file.src2.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = "${path.root}/../generated/src2.zip"
}

resource "google_cloudfunctions_function" "bq_load_job" {
  name                  = "bq_load_job"
  available_memory_mb   = 128
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.archive2.name
  service_account_email = "YOUR_SERVICE_ACCOUNT"
  runtime               = "python37"

  event_trigger { # trigger by bucekt or by topic都用這裡
    event_type = "google.storage.object.finalize" # 這裡可以使用的event_type可以從`gcloud functions event-types list`找出可以用的
    resource   = "TRIGGER_BUCKET"
    failure_policy {
      retry = true
    }
  }

  environment_variables = {
    PROJECT_ID = var.gcp_project
    TABLE_ID = "${var.gcp_project}.YOUR_DATASET.YOUR_TABLE" #concate變數及定字
    TOPIC_NAME = "YOUR_TOPIC"
  }
}
