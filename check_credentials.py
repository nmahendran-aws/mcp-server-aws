#!/usr/bin/env python3
"""
Helper script to check and validate MCP credentials and configuration
"""
import boto3
import json
from boto3.session import Session

def main():
    boto_session = Session()
    region = boto_session.region_name
    
    print(f"AWS Region: {region}\n")
    print("=" * 60)
    
    # Check Agent ARN in Parameter Store
    print("\n1. Checking Agent ARN in Parameter Store...")
    try:
        ssm_client = boto3.client('ssm', region_name=region)
        agent_arn_response = ssm_client.get_parameter(Name='/mcp_server/runtime/agent_arn')
        agent_arn = agent_arn_response['Parameter']['Value']
        
        # Validate ARN format
        if agent_arn.startswith('arn:aws:'):
            print(f"   ✓ Agent ARN: {agent_arn}")
        else:
            print(f"   ❌ Invalid ARN (placeholder detected): {agent_arn}")
            print(f"   ⚠️  You need to update this with a valid agent ARN")
            print(f"\n   To update, run:")
            print(f"   aws ssm put-parameter --name '/mcp_server/runtime/agent_arn' \\")
            print(f"       --value 'YOUR_ACTUAL_AGENT_ARN' \\")
            print(f"       --overwrite")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Check Bearer Token in Secrets Manager
    print("\n2. Checking Bearer Token in Secrets Manager...")
    try:
        secrets_client = boto3.client('secretsmanager', region_name=region)
        response = secrets_client.get_secret_value(SecretId='mcp_server/cognito/credentials')
        secret_value = response['SecretString']
        parsed_secret = json.loads(secret_value)
        
        if 'bearer_token' in parsed_secret and parsed_secret['bearer_token']:
            token_preview = parsed_secret['bearer_token'][:20] + "..." if len(parsed_secret['bearer_token']) > 20 else parsed_secret['bearer_token']
            print(f"   ✓ Bearer Token exists: {token_preview}")
        else:
            print(f"   ❌ Bearer token not found in secret")
            return False
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ All credentials validated successfully!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
