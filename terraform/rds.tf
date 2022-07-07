resource "random_password" "password" {
  length           = 16
  special          = true
  override_special = "!#$%&*()-_=+[]{}<>:?"
}

resource "aws_rds_cluster" "share_files_securely" {
  cluster_identifier     = "share-files-securely"
  engine                 = "aurora-postgresql"
  engine_mode            = "provisioned"
  engine_version         = "13.6"
  database_name          = "share_files_securely"
  master_username        = "share_files_securely"
  master_password        = random_password.password.result
  db_subnet_group_name   = aws_db_subnet_group.share_files_securely.name
  vpc_security_group_ids = [aws_security_group.share_files_securely_lambda.id]

  serverlessv2_scaling_configuration {
    max_capacity = 1.0
    min_capacity = 0.5
  }
}

resource "aws_rds_cluster_instance" "share_files_securely" {
  cluster_identifier = aws_rds_cluster.share_files_securely.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.share_files_securely.engine
  engine_version     = aws_rds_cluster.share_files_securely.engine_version
}

resource "aws_db_subnet_group" "share_files_securely" {
  name       = "share-files-securely-subnet-group"
  subnet_ids = module.vpc.private_subnet_ids

  tags = {
    Name = "share-files-securely-subnet-group"
  }
}
