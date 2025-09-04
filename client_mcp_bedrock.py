# Use the Conversation API to send a text message to Amazon Nova.

import boto3
from dotenv import load_dotenv
import requests
import json
import uuid

from botocore.exceptions import ClientError

load_dotenv()

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Set the model ID, e.g., Amazon Nova Lite.
model_id = "amazon.nova-pro-v1:0"

SERVER_URL = "http://localhost:8000/mcp"

def rpc_call(method=None, params=None, session_id=None, id=None):
    print("func rpc_call")

    payload = {
        "jsonrpc": "2.0",
        "method": method,
    }

    if id is not None:
        payload["id"] = id

    if params is not None:
        payload["params"] = params

    headers={"Content-Type": "application/json", 
            "Accept": "application/json, text/event-stream", 
            "MCP-Protocol-Version": "2025-06-18",
            "Mcp-Session-Id": session_id }

    print("---------------------------------------")
    print("headers", headers)
    print("payload", payload)
    print("---------------------------------------")

    try:
        response = requests.post(
            SERVER_URL,
            headers=headers,
            json=payload,
            stream=True,
        )

        session_id = response.headers.get("mcp-session-id")
        print("fsession_id: {session_id}")
        
        for line in response.iter_lines():
            if not line:
                continue
            if line.startswith(b"data:"):
                
                data = line[len(b"data:"):].strip()
                try:
                    event = json.loads(data.decode("utf-8"))
                    print("Event:", event)
                    
                    return session_id, event
                except Exception as e:
                    print("Could not parse:", data, e)

    except requests.exceptions.RequestException as e:
        print(f"Error communicating with MCP server: {e}")
        return None, None

def ask_bedrock(prompt: str) -> str:
    print("func ask_bedrock")
    conversation = [
        {
            "role": "user",
            "content": [{"text": prompt}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId=model_id,
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

        return response_text
    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

# ---- Demo Orchestration ----
if __name__ == "__main__":
    
    user_prompt = "add 1 to 2 and show the result"

    # Step 1: Send to LLM
    print("1. Sending to Bedrock :", user_prompt)
    llm_reply = ask_bedrock(user_prompt)
    print("2. llm_reply:", llm_reply)

    # Step 2: Intercept if it wants MCP calculator
    if "sub" in user_prompt or "add" in user_prompt:

        # 1. Initialize a session
        print("........... 1 (initialize) ........... ")
        id = str(uuid.uuid4())
        method = "initialize" #"sessions/open"
        params={"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}} 
        session_id_resp, event_resp = rpc_call(method, params=params, id=id)
        if not session_id_resp:
            raise RuntimeError("ERROR Could not open MCP session")

        # 2 notifications
        print("...........  2 (notifications/initialized)........... ")
        method = "notifications/initialized"
        notification_resp = rpc_call(method, session_id=session_id_resp, id=None)
        print("2. notification_resp:", notification_resp)

        print("...........  3 (tools) ........... ")
        id = str(uuid.uuid4())
        params= {"name": "add",
                "arguments": {"a": 1, "b": 1},
                }

        method = "tools/call"
        tools_resp = rpc_call(method, params=params, session_id=session_id_resp, id=id)
        print("3. Tools/Call result:", tools_resp)

        response_final = tools_resp
    else:
        response_final = llm_reply

    print("++++++++++++++ Final Response +++++++++++++++++++")
    print(f"FINAL RESPONSE: {response_final}")