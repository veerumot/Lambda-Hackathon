data "archive_file" "bot_file" {
  type        = "zip"
  source_file = "${path.module}/lambda.py"
  output_path = "${path.module}/bot_lambda.zip"
}

# Lambda function
resource "aws_lambda_function" "bot_lambda" {
  filename         = data.archive_file.bot_file.output_path
  function_name    = "bot_lambda_function"
  role             = var.lambda_execution_role_arn
  handler          = "lambda.lambda_handler"
  source_code_hash = data.archive_file.bot_file.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      ENVIRONMENT = "production"
      LOG_LEVEL   = "info"
    }
  }

  tags = {
    Environment = "production"
    Application = "nginx_bot"
  }
}