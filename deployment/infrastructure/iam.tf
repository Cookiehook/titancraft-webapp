resource "aws_iam_role" "ec2" {
  assume_role_policy = <<POLICY
{
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      }
    }
  ],
  "Version": "2012-10-17"
}
POLICY

  description          = "Allows EC2 instances to call AWS services on your behalf."
  managed_policy_arns  = [
    "arn:aws:iam::aws:policy/SecretsManagerReadWrite",
    "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
  ]
  max_session_duration = "3600"
  name                 = "${var.application}-ec2"
  path                 = "/"

  tags = {
    service = var.application
  }
}

resource "aws_iam_instance_profile" "iam-profile" {
  name = aws_iam_role.ec2.name
  path = "/"
  role = aws_iam_role.ec2.name
}


resource "aws_iam_role_policy_attachment" "CloudWatchLogsFullAccess" {
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
  role       = aws_iam_role.ec2.name
}

resource "aws_iam_role_policy_attachment" "SecretsManagerReadWrite" {
  policy_arn = "arn:aws:iam::aws:policy/SecretsManagerReadWrite"
  role       = aws_iam_role.ec2.name
}
