resource "aws_iam_role" "ec2_lambda_role" {
  name = "ec2-lambda-shared-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = [
            "ec2.amazonaws.com",
            "lambda.amazonaws.com"
          ]
        },
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = {
    Name        = "EC2-Lambda-Shared-Role"
    Environment = "prod"
  }
}

resource "aws_iam_policy" "full_ec2_lambda_s3" {
  name        = "FullAccess-EC2-Lambda-S3"
  description = "Provides full access to EC2, Lambda, and S3"
  policy      = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "ec2:*",
          "lambda:*",
          "s3:*",
          "logs:*"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.ec2_lambda_role.name
  policy_arn = aws_iam_policy.full_ec2_lambda_s3.arn
}


output "ec2_lambda_role_arn" {
   value = aws_iam_role.ec2_lambda_role.arn
}