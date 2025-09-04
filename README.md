# create venv
python3 -m venv .venv

# activate
source .venv/bin/activate

#install dependecies
uv add mcp
uv add 'mcp[cli]'

# run
uv run mcp dev server.py
npx @modelcontextprotocol/inspector python server.py

# run
python3 server.py

# test (agent auto)

:use the mcp calculator_streamable_http add 1 to 1 and show the result

# curl
1 Initialize Session
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
	"jsonrpc":"2.0",
	"id":1,
	"method":"initialize",
	"params":{"protocolVersion":"2025-06-18",
	"capabilities":{"tools":{}},
	"clientInfo":{"name":"test-client",
	"version":"1.0.0"}}}'

1.1 Initialize Session and get session-id
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
	"jsonrpc":"2.0",
	"id":1,
	"method":"initialize",
	"params":{"protocolVersion":"2025-06-18",
	"capabilities":{"tools":{}},
	"clientInfo":{"name":"test-client",
	"version":"1.0.0"}}}' \
  -v 2>&1 | grep -i "mcp-session-id" | cut -d' ' -f3

1.2 Initialize Session and get session-id
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
	"jsonrpc":"2.0",
	"id":1,
	"method":"sessions/open",
	"params":{"protocolVersion":"2025-06-18",
	"capabilities":{"tools":{}},
	"clientInfo":{"name":"test-client",
	"version":"1.0.0"}}}' \
  -v 2>&1 | grep -i "mcp-session-id" | cut -d' ' -f3

2. Send Initialized Notification
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: a8691f135a564c1cac7cbc5b160948a7" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

3. List Tools
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: a8691f135a564c1cac7cbc5b160948a7" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/list"}'

4. Call Add Tool
curl -X POST http://localhost:8000/mcp \
  -H "Content-Type: application/json" \
  -H "MCP-Protocol-Version: 2025-06-18" \
  -H "Accept: application/json, text/event-stream" \
  -H "Mcp-Session-Id: a8691f135a564c1cac7cbc5b160948a7" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"add","arguments":{"a":1,"b":1}}}'