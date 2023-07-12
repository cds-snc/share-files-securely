module "s3_scan_objects" {
  source = "github.com/cds-snc/terraform-modules//S3_scan_object?ref=v6.1.1"

  s3_upload_bucket_name = module.share_files_securely_bucket.s3_bucket_id

  billing_tag_value = var.billing_code
}

module "s3_scan_objects_dev" {
  source = "github.com/cds-snc/terraform-modules//S3_scan_object?ref=v6.1.5"

  s3_upload_bucket_name         = module.share_files_securely_bucket_dev.s3_bucket_id
  scan_files_assume_role_create = false

  billing_tag_value = var.billing_code
}