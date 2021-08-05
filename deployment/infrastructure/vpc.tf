resource "aws_vpc" "vpc" {
  assign_generated_ipv6_cidr_block = "false"
  cidr_block = "172.30.0.0/16"
  enable_dns_hostnames = "true"
  enable_dns_support = "true"
  instance_tenancy = "default"

  tags = {
    Name = var.application
    service = var.application
  }
}

resource "aws_security_group" "primary" {
  name = var.application
  description = "SG used by all ${var.application} resources"
  vpc_id = aws_vpc.vpc.id

  egress {
    cidr_blocks      = ["0.0.0.0/0"]
    from_port        = "0"
    ipv6_cidr_blocks = ["::/0"]
    protocol         = "tcp"
    self             = "false"
    to_port          = "65535"
  }

  egress {
    from_port = "5432"
    protocol  = "tcp"
    self      = "true"
    to_port  = "5432"
  }

  ingress {
    cidr_blocks      = ["0.0.0.0/0"]
    from_port        = "0"
    ipv6_cidr_blocks = ["::/0"]
    protocol         = "tcp"
    self             = "false"
    to_port          = "65535"
  }

  ingress {
    from_port = "5432"
    protocol  = "tcp"
    self      = "true"
    to_port   = "5432"
  }
  tags = {
    Name    = var.application
    service = var.application
  }
}

resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id = aws_vpc.vpc.id
  vpc_endpoint_type = "Interface"
  service_name = "com.amazonaws.eu-west-2.secretsmanager"
  private_dns_enabled = "true"
  subnet_ids = [
    aws_subnet.eu-west-2a-private.id,
    aws_subnet.eu-west-2b-private.id,
  ]
  security_group_ids = [
    aws_security_group.primary.id
  ]

  tags = {
    Name    = "${var.application}-secrets"
    service = var.application
  }
}
