resource "aws_cloudfront_origin_access_identity" "origin_access_identity" {
  comment = "cloudfront origin access identity"
}


resource "aws_cloudfront_distribution" "share_files_securely" {
  enabled     = true
  aliases     = ["share-files.cdssandbox.xyz"]
  price_class = "PriceClass_100"

  origin {
    domain_name = split("/", aws_lambda_function_url.share_files_securely_url.function_url)[2]
    origin_id   = aws_lambda_function_url.share_files_securely_url.function_name

    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  origin {
    domain_name = module.share_files_securely_bucket.s3_bucket_regional_domain_name
    origin_id   = "${module.share_files_securely_bucket.s3_bucket_id}-bucket"

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.origin_access_identity.cloudfront_access_identity_path
    }
  }

  default_cache_behavior {
    allowed_methods = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      headers      = ["Authorization", "Referer"]
      cookies {
        forward = "all"
      }
    }

    target_origin_id       = aws_lambda_function_url.share_files_securely_url.function_name
    viewer_protocol_policy = "redirect-to-https"
  }

  # Prevent caching of healthcheck calls
  ordered_cache_behavior {
    path_pattern    = "/healthcheck"
    allowed_methods = ["GET", "HEAD"]
    cached_methods  = ["GET", "HEAD"]

    forwarded_values {
      query_string = true
      cookies {
        forward = "none"
      }
    }

    target_origin_id       = aws_lambda_function_url.share_files_securely_url.function_name
    viewer_protocol_policy = "redirect-to-https"

    min_ttl     = 0
    default_ttl = 0
    max_ttl     = 0
    compress    = true
  }

  ordered_cache_behavior {
    path_pattern     = "/*@cds-snc.ca/*"
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "${module.share_files_securely_bucket.s3_bucket_id}-bucket"

    forwarded_values {
      query_string = true
      headers      = ["Origin"]

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "https-only"
    min_ttl                = 0
    default_ttl            = 0
    max_ttl                = 0
    compress               = true
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn      = aws_acm_certificate_validation.share_files_securely.certificate_arn
    minimum_protocol_version = "TLSv1.2_2021"
    ssl_support_method       = "sni-only"
  }

  tags = {
    CostCentre = var.billing_code
    Terraform  = true
  }
}