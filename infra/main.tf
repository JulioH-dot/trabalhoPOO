terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

resource "aws_security_group" "rds_sg" {
  name_prefix = "rds-postgres-sg-"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "Postgres Access"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "rds-postgres-sg"
  }
}

resource "aws_db_subnet_group" "main" {
  name_prefix = "rds-subnet-group-"
  subnet_ids  = data.aws_subnets.default.ids

  tags = {
    Name = "rds-subnet-group"
  }
}

resource "random_password" "db_password" {
  length  = 20
  special = true
}

resource "aws_secretsmanager_secret" "db_secret" {
  name        = "app/postgres/credentials"
  description = "Credenciais do banco PostgreSQL do app"
}

resource "aws_secretsmanager_secret_version" "db_secret_value" {
  secret_id = aws_secretsmanager_secret.db_secret.id

  secret_string = jsonencode({
    username = var.db_username
    password = random_password.db_password.result
    host     = aws_db_instance.postgres.address
    port     = aws_db_instance.postgres.port
    engine   = "postgres"
    dbname   = var.db_name
  })
}

resource "aws_db_instance" "postgres" {
  identifier              = "app-postgres-db"
  engine                  = "postgres"
  engine_version          = "15"
  instance_class          = var.instance_class
  allocated_storage       = var.allocated_storage

  db_name                 = var.db_name
  username                = var.db_username
  password                = random_password.db_password.result

  publicly_accessible     = var.publicly_accessible
  db_subnet_group_name    = aws_db_subnet_group.main.name
  vpc_security_group_ids  = [aws_security_group.rds_sg.id]
  skip_final_snapshot     = true
  multi_az                = false
  auto_minor_version_upgrade = true

  tags = {
    Name = "app-postgres-db"
  }
}
