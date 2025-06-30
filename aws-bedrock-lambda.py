import json
import boto3
import random
import string

# Replace with your real IDs
BEDROCK_AGENT_ID = "SVGQ3ZXCZR"
BEDROCK_AGENT_ALIAS_ID = "HATUAZIDM4"
REGION = "us-east-1"

session_id = ''.join(random.choices(string.ascii_letters + string.digits + "._:-", k=12))
print("🆔 Session ID:", session_id)

client = boto3.client("bedrock-agent-runtime", region_name=REGION)

def lambda_handler(event, context):
    print("Incoming event:", event)

    message = event.get("message", "")
    if not message:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "No message provided."}),
            "headers": {"Content-Type": "application/json"}
        }

    try:
        response = client.invoke_agent(
            enableTrace=True,
            agentId=BEDROCK_AGENT_ID,
            agentAliasId=BEDROCK_AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText= message
        )

        chunks = []
        for part in response["completion"]:
            chunk = part.get("chunk", {}).get("bytes")
            if chunk:
                chunks.append(chunk.decode("utf-8"))

        final_response = "".join(chunks).strip()
        print("🧠 Agent response:", final_response)

        result = {
            "response": final_response
        }

        if "sudo" in final_response:
            lines = final_response.splitlines()
            for line in lines:
                if line.strip().startswith("sudo"):
                    result["command"] = line.strip()
                    break

        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {"Content-Type": "application/json"}
        }

    except Exception as e:
        print("❌ Error calling Bedrock Agent:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Failed to invoke Bedrock Agent: {str(e)}"}),
            "headers": {"Content-Type": "application/json"}
        }
