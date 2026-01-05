# MCP Server

A TypeScript-based MCP (Model Context Protocol) server for AWS Bedrock Agentcore.

## Quick Start

### Prerequisites

- Node.js (v20 or higher)
- Python 3.13+
- AWS CLI configured with credentials
- AWS Bedrock Agentcore Starter Toolkit

### Installation

1. **Install Node.js dependencies:**
```bash
npm install
```

2. **Install Python dependencies:**
```bash
pip3 install boto3>=1.26.0
pip3 install bedrock-agentcore-starter-toolkit
```

### Build and Run Locally

```bash
# Build TypeScript
npm run build

# Run the server
npm start
```

The server will start on port 3001 at the `/mcp` endpoint.

## AWS Bedrock Agentcore Deployment

### Prerequisites Setup

The following AWS resources are required:
- Amazon Cognito User Pool for authentication
- IAM Role for Agentcore execution
- Bedrock Agentcore runtime

### Option 1: Automated Configuration (Recommended)

Use the provided helper script to automatically set up all required resources and configure your MCP server:

```bash
# Build your TypeScript project first
npm run build

# Run the automated configuration
python3 configure_mcp.py
```

This script will:
1. Check for existing Cognito configuration or create a new one
2. Check for existing IAM role or create a new one
3. Run `agentcore configure` with correct parameters
4. Store configuration in AWS Parameter Store and Secrets Manager

### Option 2: Manual Configuration

If you prefer manual setup, follow these steps:

#### Step 1: Set up Cognito (if not already done)
```python
from utils import setup_cognito_user_pool
cognito_config = setup_cognito_user_pool()
```

#### Step 2: Create IAM Role (if not already done)
```python
from utils import create_agentcore_role
agentcore_iam_role = create_agentcore_role('mcp_server')
role_arn = agentcore_iam_role['Role']['Arn']
```

#### Step 3: Configure Agentcore

```bash
agentcore configure \
  --protocol MCP \
  --entrypoint dist/index.js \
  --execution-role <iam-role-arn> \
  --authorizer-config '{"oidcDiscoveryUrl": "<cognito-discovery-url>", "allowedAudiences": ["<client-id>"], "allowedClients": ["<client-id>"]}' \
  --name mcp_server \
  --region us-east-1
```

#### Step 4: Deploy
```bash
agentcore deploy
```

## Configuration Files

### Helper Scripts

- **`configure_mcp.py`** - Automated configuration script that sets up all AWS resources and configures the MCP server
- **`check_credentials.py`** - Validates MCP credentials and AWS configuration
- **`utils.py`** - Utility functions for Cognito and IAM setup

### MCP Client

- **`my_mcp_client_remote.py`** - Python client to connect to deployed MCP server

## Important Validation Rules

### Agent Name Requirements
- Must start with a letter
- Can only contain: **letters, numbers, underscores**
- Must be 1-48 characters long
- ❌ **Hyphens are NOT allowed** (use `mcp_server`, not `mcp-server`)

### Authorizer Config Format
The `--authorizer-config` parameter requires a JSON string with:
```json
{
  "oidcDiscoveryUrl": "https://cognito-idp.{region}.amazonaws.com/{pool-id}/.well-known/openid-configuration",
  "allowedAudiences": ["<client-id>"],
  "allowedClients": ["<client-id>"]
}
```

## Troubleshooting

### Error: "No such option: --discovery-url"
**Solution:** Use `--authorizer-config` with JSON format instead of separate `--discovery-url` and `--client-id` parameters.

### Error: "Invalid agent name"
**Solution:** Ensure agent name uses underscores instead of hyphens (e.g., `mcp_server` not `mcp-server`).

### Error: "Entrypoint file not found"
**Solution:** Run `npm run build` first to compile TypeScript to JavaScript in the `dist/` directory.

### Error: "Invalid Agent ARN"
**Solution:** Update the Parameter Store with a valid agent ARN:
```bash
aws ssm put-parameter \
  --name '/mcp_server/runtime/agent_arn' \
  --value 'YOUR_ACTUAL_AGENT_ARN' \
  --overwrite \
  --region us-east-1
```

## Project Structure

```
mcp-server/
├── src/
│   ├── index.ts              # Main server entry point
│   └── server.ts             # MCP server implementation
├── dist/                     # Compiled JavaScript output
├── configure_mcp.py          # Automated configuration script
├── check_credentials.py      # Credential validation script
├── utils.py                  # AWS utility functions
├── my_mcp_client_remote.py   # Python MCP client
├── requirements.txt          # Python dependencies
├── package.json              # Node.js configuration
├── tsconfig.json             # TypeScript configuration
├── Dockerfile                # Docker configuration
└── README.md                 # This file
```

## Additional Resources

- [IAM_PERMISSIONS_GUIDE.md](IAM_PERMISSIONS_GUIDE.md) - Detailed IAM permissions required
- [POSTMAN_GUIDE.md](POSTMAN_GUIDE.md) - Testing with Postman

## Deployment Status

### ✅ Successfully Deployed

The MCP server has been deployed to AWS Bedrock Agentcore:

- **Agent Name**: `mcp_server`
- **Agent ARN**: `arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mcp_server-6fH7Xm6UtL`
- **Status**: Ready
- **Endpoint**: `arn:aws:bedrock-agentcore:us-east-1:471727841202:runtime/mcp_server-6fH7Xm6UtL/runtime-endpoint/DEFAULT`
- **Region**: us-east-1
- **Build Time**: 1m 29s
- **Deployed**: 2026-01-05 23:06:49 UTC

View in AWS Console:
- [Bedrock AgentCore](https://us-east-1.console.aws.amazon.com/bedrock/home?region=us-east-1#/agentcore)
- [GenAI Observability Dashboard](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#gen-ai-observability/agent-core)

### ⚠️ Known Issue: Authentication

**Problem**: Invocation fails with 401 Unauthorized due to JWT audience claim mismatch.

**Error Message**:
```
Claim 'aud' value mismatch with configuration.
```

**Root Cause**: The Cognito-generated JWT access token doesn't include an `aud` (audience) claim that matches the server's expected audience configuration.

**Workaround Options**:

1. **Configure Cognito Resource Server** (Recommended):
   - Create a Resource Server in the Cognito User Pool
   - Define custom scopes
   - Update App Client to request tokens with proper audience

2. **Use ID Token Instead of Access Token**:
   - ID tokens automatically include `aud` claim set to `client_id`
   - Modify authentication to use ID tokens

3. **Adjust Server Configuration**:
   - Update `.bedrock_agentcore.yaml` authorization config
   - Redeploy with modified settings

**Testing Status**:
- ✅ Server deployment successful
- ✅ Server status: Ready
- ❌ Client authentication: Requires configuration fix
- ❌ Tool invocation: Blocked by auth issue

**Related Files**:
- [`.bedrock_agentcore.yaml`](.bedrock_agentcore.yaml) - Server configuration
- [`my_mcp_client_remote.py`](my_mcp_client_remote.py) - Python client (needs auth fix)
- [`test_mcp_curl.sh`](test_mcp_curl.sh) - Direct HTTP test script

## CloudWatch Logs

View runtime logs:
```bash
aws logs tail /aws/bedrock-agentcore/runtimes/mcp_server-6fH7Xm6UtL-DEFAULT \
  --log-stream-name-prefix "2026/01/05/[runtime-logs]" \
  --follow
```

## License

ISC
