import re
import time
import boto3
import json
import subprocess

# === Configuration ===
LOG_FILE = "/var/log/nginx/access.log"
LAMBDA_FUNCTION_NAME = "bot_lambda_function"  # Replace with your actual Lambda function name

log_pattern = re.compile(
    r'"(?P<method>GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS) (?P<path>.*?) HTTP/.*?" (?P<status>\d{3})'
)

# Initialize AWS Lambda client
lambda_client = boto3.client("lambda", region_name="us-east-1")


def trigger_lambda_and_get_response(method, path, status, raw_line):
    message = f"{method} {path} => {status}"
    print(f"🚨 Sending message to Lambda: {message}")
    try:
        response = lambda_client.invoke(
            FunctionName=LAMBDA_FUNCTION_NAME,
            InvocationType="RequestResponse",
            Payload=json.dumps({ "message": message }).encode("utf-8"),
        )
        result_payload = response["Payload"].read().decode("utf-8")
        raw_result = json.loads(result_payload)

        # Parse JSON inside the "body" field
        result = json.loads(raw_result["body"]) if "body" in raw_result else raw_result
        print("🧠 Lambda response:", result)
        return result
    except Exception as e:
        print(f"❌ Failed to invoke Lambda: {e}")
        return None

def execute_command(command: str):
    """Run the command securely (e.g., restart a service)."""
    print(f"⚙️ Executing command: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"✅ Command output:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed:\n{e.stderr.decode()}")


def follow_file(file_path):
    with open(file_path, "r") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line


def run_bot():
    print("🛡️ Watching NGINX logs for 5xx errors (plain text to Lambda)...")
    for line in follow_file(LOG_FILE):
        match = log_pattern.search(line)
        if match:
            status = int(match.group("status"))
            if 500 <= status < 600:
                method = match.group("method")
                path = match.group("path")
                raw_log = line.strip()
                response = trigger_lambda_and_get_response(method, path, status, raw_log)
                print(response)
                if response and "command" in response:
                    execute_command(response["command"])
                else:
                    print("ℹ️ No command returned from Lambda.")


if __name__ == "__main__":
    run_bot()