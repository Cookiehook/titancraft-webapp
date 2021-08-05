resource "aws_route53_record" "api" {
  name    = "titancraft.cookiehook.com"
  records = [aws_alb.alb.dns_name]
  ttl     = "300"
  type    = "CNAME"
  zone_id = data.aws_route53_zone.cookiehook.zone_id
}
