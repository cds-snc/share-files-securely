/*
module "api" {
  source                 = "github.com/cds-snc/terraform-modules?ref=v3.0.5//lambda"
  name                   = "share_files_securely"
  billing_tag_value      = var.billing_code
  ecr_arn                = aws_ecr_repository.share_files_securely.arn
  enable_lambda_insights = true
  image_uri              = "${aws_ecr_repository.share_files_securely.repository_url}:latest"
  memory                 = 512
  timeout                = 300
}
*/