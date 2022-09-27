module "share_files_securely_lambda" {
  source                 = "github.com/cds-snc/terraform-modules?ref=v3.0.18//lambda"
  name                   = "share_files_securely"
  billing_tag_value      = var.billing_code
  ecr_arn                = aws_ecr_repository.share_files_securely.arn
  enable_lambda_insights = true
  image_uri              = "${aws_ecr_repository.share_files_securely.repository_url}:latest"
  memory                 = 512
  timeout                = 300


  vpc = {
    security_group_ids = [aws_security_group.share_files_securely_lambda.id]
    subnet_ids         = module.vpc.private_subnet_ids
  }

  environment_variables = {
    APP_URL       = "https://share-files.cdssandbox.xyz"
    AWS_S3_BUCKET = module.share_files_securely_bucket.s3_bucket_id
    DB_CONNECTION = "postgres"
    DB_HOST       = aws_rds_cluster.share_files_securely.endpoint
    DB_USERNAME   = aws_rds_cluster.share_files_securely.master_username
    DB_DATABASE   = aws_rds_cluster.share_files_securely.database_name
    DB_PASSWORD   = random_password.password.result
    DB_PORT       = 5432
  }

  policies = [
    data.aws_iam_policy_document.share_files_securely_lambda_policies.json,
  ]
}

resource "aws_lambda_alias" "share_files_securely" {
  name             = "latest"
  description      = "Alias for traffic shifting"
  function_name    = module.share_files_securely_lambda.function_arn
  function_version = module.share_files_securely_lambda.function_version
  depends_on = [
    module.share_files_securely_lambda
  ]

  lifecycle {
    ignore_changes = [
      function_version,
    ]
  }
}

resource "aws_lambda_function_url" "share_files_securely_url" {
  # checkov:skip=CKV_AWS_258: Lambda function url auth is handled at the API level
  function_name      = module.share_files_securely_lambda.function_name
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    max_age           = 86400
  }
}
  
resource "aws_lambda_function_url" "share_files_securely_url_alias" {
  # checkov:skip=CKV_AWS_258: Lambda function url auth is handled at the API level
  function_name      = "${module.share_files_securely_lambda.function_name}:${aws_lambda_alias.share_files_securely.name}"
  authorization_type = "NONE"

  cors {
    allow_credentials = true
    allow_origins     = ["*"]
    allow_methods     = ["*"]
    max_age           = 86400
  }
}
