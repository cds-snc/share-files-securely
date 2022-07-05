resource "aws_ecr_repository" "share_files_securely" {
  name                 = "share-files-securely"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}