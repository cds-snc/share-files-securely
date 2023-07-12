module "share_files_securely_bucket" {
  source            = "github.com/cds-snc/terraform-modules//S3?ref=v6.1.1"
  billing_tag_value = var.billing_code
  bucket_name       = "share-files-securely"

  versioning = {
    enabled = true
  }

  lifecycle_rule = [{
    id      = "expire"
    enabled = true
    expiration = {
      days = 30
    }
  }]
}

resource "aws_s3_bucket_cors_configuration" "share_files_securely_bucket" {
  bucket = module.share_files_securely_bucket.s3_bucket_id


  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE"]
    allowed_origins = ["*"]
    expose_headers  = []
  }
}

module "share_files_securely_bucket_dev" {
  source            = "github.com/cds-snc/terraform-modules//S3?ref=v6.1.1"
  billing_tag_value = var.billing_code
  bucket_name       = "share-files-securely-dev"

  versioning = {
    enabled = true
  }

  lifecycle_rule = [{
    id      = "expire"
    enabled = true
    expiration = {
      days = 30
    }
  }]
}

resource "aws_s3_bucket_cors_configuration" "share_files_securely_bucket_dev" {
  bucket = module.share_files_securely_bucket_dev.s3_bucket_id


  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE"]
    allowed_origins = ["*"]
    expose_headers  = []
  }
}