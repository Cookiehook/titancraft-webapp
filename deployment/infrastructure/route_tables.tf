resource "aws_internet_gateway" "apigw" {
  vpc_id = aws_vpc.vpc.id

  tags = {
    Name    = var.application
    service = var.application
  }
}

// Route Tables
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.apigw.id
  }
  tags = {
    Name    = "${var.application}-public"
    service = var.application
  }
}

resource "aws_route_table" "eu-west-2a-private" {
  vpc_id = aws_vpc.vpc.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.eu-west-2a.id
  }
  tags = {
    Name    = "${var.application}-eu-west-2a-private"
    service = var.application

  }
}

// Route Table associations with subnets / VPC
resource "aws_route_table_association" "eu-west-2a-private" {
  route_table_id = aws_route_table.eu-west-2a-private.id
  subnet_id      = aws_subnet.eu-west-2a-private.id
}

resource "aws_route_table_association" "eu-west-2a-public" {
  route_table_id = aws_route_table.public.id
  subnet_id      = aws_subnet.eu-west-2a-public.id
}

resource "aws_route_table_association" "eu-west-2b-public" {
  route_table_id = aws_route_table.public.id
  subnet_id      =  aws_subnet.eu-west-2b-public.id
}
