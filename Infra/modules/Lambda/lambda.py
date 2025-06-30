import json
import boto3
import os

# S3 location of your error definitions
BUCKET_NAME = "bot-logs-data"
OBJECT_KEY = "bot_data.json"

s3 = boto3.client("s3")

def load_error_data():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=OBJECT_KEY)
        content = response["Body"].read().decode("utf-8")
        return json.loads(content)
    except Exception as e:
        print(f"❌ Failed to load error data: {e}")
        return {}

def lambda_handler(event, context):
    print("Incoming event:", event)
    message = event.get("message", "").strip()
    if not message:
        return {
            "statusCode": 400,
            "body": json.dumps({ "error": "No message provided" }),
            "headers": { "Content-Type": "application/json" }
        }
    error_data = load_error_data()
    match = error_data.get(message)
    if match:
        return {
            "statusCode": 200,
            "body": json.dumps(match),
            "headers": { "Content-Type": "application/json" }
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": f"No fix found for: {message}",
                "command": ""
            }),
            "headers": { "Content-Type": "application/json" }
        }
