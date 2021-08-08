resource "aws_subnet" "eu-west-2a-public" {
  vpc_id                          = aws_vpc.vpc.id
  availability_zone               = "eu-west-2a"
  cidr_block                      = "172.30.1.0/24"

  tags = {
    Name    = "${var.application}-eu-west-2a-public"
    service = var.application
  }
}

resource "aws_subnet" "eu-west-2a-private" {
  vpc_id                          = aws_vpc.vpc.id
  availability_zone               = "eu-west-2a"
  cidr_block                      = "172.30.2.0/24"

  tags = {
    Name    = "${var.application}-eu-west-2a-private"
    service = var.application
  }
}

resource "aws_subnet" "eu-west-2b-public" {
  vpc_id                          = aws_vpc.vpc.id
  availability_zone               = "eu-west-2b"
  cidr_block                      = "172.30.3.0/24"

  tags = {
    Name    = "${var.application}-eu-west-2b-public"
    service = var.application
  }
}

resource "aws_subnet" "eu-west-2b-private" {
  vpc_id                          = aws_vpc.vpc.id
  availability_zone               = "eu-west-2b"
  cidr_block                      = "172.30.4.0/24"

  tags = {
    Name    = "${var.application}-eu-west-2b-private"
    service = var.application
  }
}

resource "aws_eip" "eu-west-2a" {
  vpc = "true"
  network_border_group = "eu-west-2"
  public_ipv4_pool     = "amazon"

  tags = {
    Name    = "${var.application}-eu-west-2a"
    service = var.application
  }
}

resource "aws_nat_gateway" "eu-west-2a" {
  allocation_id     = aws_eip.eu-west-2a.id
  connectivity_type = "public"
  subnet_id         = aws_subnet.eu-west-2a-public.id
  tags = {
    Name    = "${var.application}-eu-west-2a"
    service = var.application
  }
}
