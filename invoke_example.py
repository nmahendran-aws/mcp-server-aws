#!/usr/bin/env python3
"""
Example script showing how to invoke the deployed MCP server directly
"""
import boto3
import json
import requests
from utils import reauthenticate_user

def invoke_mcp_server():
    """Invoke the deployed MCP server"""
    region = 'us-east-1'
    
    # Get the runtime ARN from Parameter Store
    ssm_client = boto3.client('ssm', region_name=region)
    agent_arn_response = ssm_client.get_parameter(Name='/mcp_server/runtime/agent_arn')
    agent_arn = agent_arn_response['Parameter']['Value']
    
    # Get Cognito credentials
    secrets_client = boto3.client('secretsmanager', region_name=region)
    response = secrets_client.get_secret_value(SecretId='mcp_server/cognito/credentials')
    secret_value = response['SecretString']
    parsed_secret = json.loads(secret_value)
    client_id = parsed_secret['client_id']
    
    # Get fresh bearer token
    bearer_token = reauthenticate_user(client_id)
    
    print(f"Agent ARN: {agent_arn}")
    print(f"Token retrieved: {bearer_token[:20]}...")
    
    # Construct the endpoint URL
    encoded_arn = agent_arn.replace(':', '%3A').replace('/', '%2F')
    endpoint_url = f"https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
    
    # Prepare the request
    headers = {
        "authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # MCP request payload (jsonrpc format)
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/list",
        "params": {}
    }
    
    print(f"\nInvoking: {endpoint_url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    # Make the request
    response = requests.post(endpoint_url, headers=headers, json=payload)
    
    print(f"\nStatus Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ Success!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Error: {response.text}")

if __name__ == "__main__":
    invoke_mcp_server()
