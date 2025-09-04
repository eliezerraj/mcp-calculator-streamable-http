import requests
import uuid
import json

SERVER_URL = "http://localhost:8000/mcp"

def rpc_call(method=None, params=None, session_id=None, id=None):

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
    print("++++++++++++++ 1 (initialize) +++++++++++++++++++")
    id = str(uuid.uuid4())
    method = "initialize" #"sessions/open"
    params={"protocolVersion":"2025-06-18","capabilities":{"tools":{}},"clientInfo":{"name":"test-client","version":"1.0.0"}} 
    session_id_resp, event_resp = rpc_call(method, params=params, id=id)

    print("1. session_id_resp:", session_id_resp)
    print("1. event_resp:", event_resp)

    # 2 notifications
    print("+++++++++++++ 2 (notifications/initialized) ++++++++++++++++++++")
    method = "notifications/initialized"
    notification_resp = rpc_call(method, session_id=session_id_resp, id=None)
    print("2. notification_resp:", notification_resp)

    # 3. List tools
    print("+++++++++++++ 3 (tools/list) ++++++++++++++++++++")
    id = str(uuid.uuid4())
    method = "tools/list"
    list_resp = rpc_call(method, session_id=session_id_resp, id=id)
    print("3. Tools available:", list_resp)

    # 4. Tools call - add
    print("+++++++++++++ 4 (add) ++++++++++++++++++++")
    id = str(uuid.uuid4())
    method = "tools/call"
    params= {"name": "add",
            "arguments": {"a": 1, "b": 1},
            }
    tools_resp = rpc_call(method, params=params, session_id=session_id_resp, id=id)
    print("3. Tools/Call result:", tools_resp)
    

if __name__ == "__main__":
    main()
