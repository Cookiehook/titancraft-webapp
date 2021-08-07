variable application {}
variable branch {}

data "aws_vpc" "vpc" {
  filter {
    name = "tag:Name"
    values = [
      var.application]
  }
}

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
  filter {
    name = "tag:Name"
    values = [
      var.application]
  }
}

data "aws_acm_certificate" "cookiehook" {
  domain = "*.cookiehook.com"
}

data "aws_route53_zone" "cookiehook" {
  name = "cookiehook.com"
}

data "aws_iam_instance_profile" "iam-profile" {
  name = "${var.application}-ec2"
}
