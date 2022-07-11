resource "aws_route53_zone" "share_files_securely" {
  name = "share-files.cdssandbox.xyz"

  tags = {
    "CostCentre" = var.billing_code
  }
}

resource "aws_route53_record" "share_files_securely_A" {
  zone_id = aws_route53_zone.share_files_securely.zone_id
  name    = "share-files.cdssandbox.xyz"
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.share_files_securely.domain_name
    zone_id                = aws_cloudfront_distribution.share_files_securely.hosted_zone_id
    evaluate_target_health = false
  }
}

resource "aws_route53_health_check" "share_files_securely_A" {
  fqdn              = aws_route53_record.share_files_securely_A.fqdn
  port              = 443
  type              = "HTTPS"
  resource_path     = "/healthcheck"
  failure_threshold = "5"
  request_interval  = "30"

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}