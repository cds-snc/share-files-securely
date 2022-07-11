data "aws_iam_policy_document" "share_files_securely_lambda_policies" {

  statement {

    effect = "Allow"

    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]

    resources = [
      "arn:aws:logs:ca-central-1:${data.aws_caller_identity.current.account_id}:log-group:*"
    ]
  }

  statement {

    effect = "Allow"

    actions = [
      "s3:*"
    ]
    resources = [
      module.share_files_securely_bucket.s3_bucket_arn,
      "${module.share_files_securely_bucket.s3_bucket_arn}/*",
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameters",
    ]
    resources = [
      "arn:aws:ssm:ca-central-1:${data.aws_caller_identity.current.account_id}:parameter/share-files-securely-config"
    ]
  }

  statement {

    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]
    resources = [
      module.share_files_securely_lambda.function_arn
    ]
  }
}