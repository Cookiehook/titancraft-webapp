resource "aws_route53_record" "rds" {
  name    = "${var.application}-rds.cookiehook.com"
  records = [aws_db_instance.db.address]
  ttl     = "300"
  type    = "CNAME"
  zone_id = data.aws_route53_zone.cookiehook.zone_id
}