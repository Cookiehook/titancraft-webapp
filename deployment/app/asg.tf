resource "aws_autoscaling_group" "asg" {
  name = aws_launch_configuration.launch_configuration.name
  min_size = "1"
  max_size = "5"
  desired_capacity = "1"
  wait_for_capacity_timeout = "10m"
  launch_configuration = aws_launch_configuration.launch_configuration.name
  vpc_zone_identifier = [
    data.aws_subnet.eu-west-2a-private.id,
  ]
  target_group_arns = [
    aws_lb_target_group.target-group.arn
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_launch_configuration" "launch_configuration" {
  name = "titancraft-${replace(timestamp(), ":", "")}"
  instance_type = "t2.medium"
  image_id = data.aws_ami.amazon-linux.id
  iam_instance_profile = data.aws_iam_instance_profile.iam-profile.arn
  user_data = data.template_file.userdata.rendered
  security_groups = [data.aws_security_group.primary.id]
}

data "aws_ami" "amazon-linux" {
  most_recent = true
  owners = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "template_file" "userdata" {
  template = file("${path.module}/templates/userdata.sh")
  vars = {
    aws_region = "eu-west-2"
    docker_tag = var.branch
  }
}
