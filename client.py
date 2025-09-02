import requests
import uuid
import json

SERVER_URL = "http://localhost:8000/mcp"

def rpc_call(method, params=None, session_id=None, id=None):

    payload = {
        "jsonrpc": "2.0",
        "id": id or str(uuid.uuid4()),
        "method": method,
        "params": params or {}
    }

    # include sessionId in params if required
    if session_id and "sessionId" not in payload["params"]:
        payload["params"]["sessionId"] = session_id

    print("---------------------------------------")
    print("payload", payload)
    print("---------------------------------------")
    try:
        response = requests.post(
            SERVER_URL,
            headers={"Content-Type": "application/json", 
                    "Accept": "application/json, text/event-stream", 
                    "MCP-Protocol-Version": "2025-06-18",
                    },
            json=payload,
            stream=True,
        )

        session_id = response.headers.get("mcp-session-id")
        print("=>extracted session_id:", session_id)
        
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

def main():
    # 1. Initialize a session
    session_id_resp, event_resp = rpc_call("initialize", {"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}})
    print("---------------------------------------")

    print("session_id_resp:", session_id_resp)
    print("event_resp:", event_resp)

    if not session_id_resp:
        print("Failed to get sessionId")
        return
    
    # 2. List tools
    list_resp = rpc_call("tools/list", session_id=session_id)
    print("Tools available:", list_resp)
    
    """
    # 3. Call `add` tool
    add_resp = rpc_call(
        "tools/call",
        {
            "name": "add",
            "arguments": {"a": 5, "b": 3}
        },
        session_id=session_id
    )
    print("Add result:", add_resp)

    # 4. Call `divide` tool
    div_resp = rpc_call(
        "tools/call",
        {
            "name": "divide",
            "arguments": {"a": 10, "b": 2}
        },
        session_id=session_id
    )
    print("Divide result:", div_resp)"""


if __name__ == "__main__":
    main()
