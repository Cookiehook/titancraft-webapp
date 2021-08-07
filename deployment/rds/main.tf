variable application {}

data "aws_subnet" "eu-west-2a-public" {
  filter {
    name = "tag:Name"
    values = ["${var.application}-eu-west-2a-public"]
  }
}

data "aws_subnet" "eu-west-2a-private" {
  filter {
    name = "tag:Name"
    values = ["${var.application}-eu-west-2a-private"]
  }
}

data "aws_subnet" "eu-west-2b-public" {
  filter {
    name = "tag:Name"
    values = ["${var.application}-eu-west-2b-public"]
  }
}

data "aws_subnet" "eu-west-2b-private" {
  filter {
    name = "tag:Name"
    values = ["${var.application}-eu-west-2b-private"]
  }
}

data "aws_iam_role" "rds-monitoring" {
  name = "rds-monitoring-role"
}

data "aws_security_group" "primary" {
  name = var.application
}

data "aws_acm_certificate" "cookiehook" {
  domain = "*.cookiehook.com"
}

data "aws_route53_zone" "cookiehook" {
  name = "cookiehook.com"
}
