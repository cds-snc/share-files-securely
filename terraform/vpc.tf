module "vpc" {
  source             = "github.com/cds-snc/terraform-modules//vpc?ref=v6.1.1"
  name               = "share-files-securely"
  billing_tag_value  = var.billing_code
  high_availability  = true
  block_ssh          = true
  block_rdp          = true
  single_nat_gateway = true

  allow_https_request_out          = true
  allow_https_request_out_response = true
  allow_https_request_in           = true
  allow_https_request_in_response  = true
}

resource "aws_security_group" "share_files_securely_lambda" {
  # checkov:skip=CKV2_AWS_5: False-positive, SG is attached in lambda.tf

  name        = "share_files_securely_sg"
  description = "SG for the Share Files Securely lambda"

  vpc_id = module.vpc.vpc_id

  tags = {
    Name       = "share_files_securely_sg"
    CostCentre = var.billing_code
    Terraform  = true
  }
}

resource "aws_security_group_rule" "lambda_port_443_egress" {
  description       = "Security group rule for Lambda egress to port 443"
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.share_files_securely_lambda.id
}

resource "aws_security_group_rule" "lambda_port_5432_egress" {
  description              = "Security group rule for Lambda egress to port 5432 (postgres)"
  type                     = "egress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.share_files_securely_lambda.id
  source_security_group_id = aws_security_group.share_files_securely_lambda.id
}

resource "aws_security_group_rule" "lambda_port_443_ingress" {
  description       = "Security group rule for Lambda ingress to port 443"
  type              = "ingress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]
  security_group_id = aws_security_group.share_files_securely_lambda.id
}

resource "aws_security_group_rule" "lambda_port_5432_ingress" {
  description              = "Security group rule for Lambda ingress to port 5432 (postgres)"
  type                     = "ingress"
  from_port                = 5432
  to_port                  = 5432
  protocol                 = "tcp"
  security_group_id        = aws_security_group.share_files_securely_lambda.id
  source_security_group_id = aws_security_group.share_files_securely_lambda.id
}