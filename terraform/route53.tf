resource "aws_route53_zone" "share_files_securely" {
  name = "share-files.cdssandbox.xyz"

  tags = {
    "CostCentre" = var.billing_code
  }
}