resource "aws_alb" "alb" {
  name                       = "titancraft"
  drop_invalid_header_fields = "false"
  enable_deletion_protection = "false"
  enable_http2               = "true"
  idle_timeout               = "600"
  internal                   = "false"
  ip_address_type            = "ipv4"
  load_balancer_type         = "application"

  security_groups = [
    data.aws_security_group.primary.id
  ]
  subnets = [
    data.aws_subnet.eu-west-2a-public.id,
    data.aws_subnet.eu-west-2b-public.id,
  ]

  tags = {
    service = "titancraft"
  }
}

resource "aws_lb_listener" "listener" {
  certificate_arn = data.aws_acm_certificate.cookiehook.arn

  default_action {
    target_group_arn = aws_lb_target_group.target-group.arn
    type             = "forward"
  }

  load_balancer_arn = aws_alb.alb.arn
  port              = "443"
  protocol          = "HTTPS"
  ssl_policy        = "ELBSecurityPolicy-2016-08"
}

resource "aws_lb_listener_rule" "listener-rule" {
  listener_arn = aws_lb_listener.listener.arn
  priority     = "50000"

  action {
    target_group_arn = aws_lb_target_group.target-group.arn
    type             = "forward"
  }

  condition {
    path_pattern {
      values = ["*"]
    }
  }
}

resource "aws_lb_target_group" "target-group" {
  name = "titancraft"
  port = 5000
  protocol = "HTTP"
  vpc_id = data.aws_vpc.vpc.id

  health_check {
    path = "/health"
    protocol = "HTTP"
    interval = "20"
    timeout = "5"
    healthy_threshold = "5"
    unhealthy_threshold = "2"
  }
}
