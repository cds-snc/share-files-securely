module "s3_scan_objects" {
  source = "github.com/cds-snc/terraform-modules//S3_scan_object?ref=v7.0.0"

  s3_upload_bucket_names = [
    module.share_files_securely_bucket.s3_bucket_id,
    module.share_files_securely_bucket_dev.s3_bucket_id
  ]

  billing_tag_value = var.billing_code
}
