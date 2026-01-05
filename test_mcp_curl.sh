#!/bin/bash
# Test MCP server with direct HTTP request

# Get bearer token
BEARER_TOKEN=$(python3 -c "from utils import reauthenticate_user; print(reauthenticate_user('64pfmi681vf104vacrl493kptn'))")

# MCP endpoint
URL="https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/arn%3Aaws%3Abedrock-agentcore%3Aus-east-1%3A471727841202%3Aruntime%2Fmcp_server-6fH7Xm6UtL/invocations?qualifier=DEFAULT"

# MCP request payload
PAYLOAD='{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}'

echo "Testing MCP server..."
echo "URL: $URL"
echo "Token preview: ${BEARER_TOKEN:0:30}..."
echo ""

# Make request
curl -X POST "$URL" \
  -H "authorization: Bearer $BEARER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d "$PAYLOAD" \
  -v

echo ""
echo "Done"
