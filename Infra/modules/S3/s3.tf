resource "aws_s3_bucket" "bot-logs-data" {
  bucket = "bot-logs-data"  # Replace with a unique bucket name
}

resource "aws_s3_bucket_ownership_controls" "bot-logs-data" {
  bucket = aws_s3_bucket.bot-logs-data.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "bot-logs-data" {
  depends_on = [aws_s3_bucket_ownership_controls.bot-logs-data]

  bucket = aws_s3_bucket.bot-logs-data.id
  acl    = "private"
}

resource "aws_s3_object" "data" {
  bucket = aws_s3_bucket.bot-logs-data.bucket
  key    = "bot_data.json"  # Replace with your desired object key
  source = "/Users/madhurigorantla/github/Lambda-Hackathon/bot/bot_data.json"  # Replace with the path to your local file
  etag   = filemd5("/Users/madhurigorantla/github/Lambda-Hackathon/bot/bot_data.json") # Optional: ETag for object versioning
}

output "aws_s3_bucket_bot-logs-data_arn"{
   value = aws_s3_bucket.bot-logs-data.arn
}