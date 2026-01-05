#!/usr/bin/env python3
"""
Helper script to configure MCP with Bedrock Agentcore
This script retrieves the necessary configuration values and runs the agentcore configure command
"""
import boto3
import json
import subprocess
import sys
from boto3.session import Session
from utils import setup_cognito_user_pool, create_agentcore_role

def get_or_create_configuration():
    """Get existing configuration or create new one"""
    boto_session = Session()
    region = boto_session.region_name
    
    print("=" * 70)
    print("MCP AgentCore Configuration Helper")
    print("=" * 70)
    
    # Check if configuration already exists
    print("\n1. Checking existing configuration...")
    
    try:
        ssm_client = boto3.client('ssm', region_name=region)
        secrets_client = boto3.client('secretsmanager', region_name=region)
        
        # Try to get existing cognito config
        try:
            response = secrets_client.get_secret_value(SecretId='mcp_server/cognito/credentials')
            secret_value = response['SecretString']
            cognito_config = json.loads(secret_value)
            print("   ✓ Found existing Cognito configuration")
        except secrets_client.exceptions.ResourceNotFoundException:
            print("   ⚠️  Cognito configuration not found, creating new...")
            cognito_config = setup_cognito_user_pool()
            if not cognito_config:
                print("   ❌ Failed to create Cognito configuration")
                return None
        
        # Try to get existing IAM role
        try:
            iam_response = ssm_client.get_parameter(Name='/mcp_server/iam/role_arn')
            role_arn = iam_response['Parameter']['Value']
            print("   ✓ Found existing IAM role")
        except ssm_client.exceptions.ParameterNotFound:
            print("   ⚠️  IAM role not found, creating new...")
            agent_name = "mcp_server"  # Must use underscores, not hyphens
            agentcore_iam_role = create_agentcore_role(agent_name)
            role_arn = agentcore_iam_role['Role']['Arn']
            # Store it for future use
            ssm_client.put_parameter(
                Name='/mcp_server/iam/role_arn',
                Value=role_arn,
                Type='String',
                Overwrite=True
            )
            print(f"   ✓ Created IAM role: {role_arn}")
        
        return {
            'discovery_url': cognito_config.get('discovery_url'),
            'client_id': cognito_config.get('client_id'),
            'role_arn': role_arn,
            'region': region
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def run_agentcore_configure(config):
    """Run the agentcore configure command with the retrieved configuration"""
    
    print("\n2. Configuration values:")
    print(f"   Discovery URL: {config['discovery_url']}")
    print(f"   Client ID: {config['client_id']}")
    print(f"   Execution Role: {config['role_arn']}")
    print(f"   Region: {config['region']}")
    
    # Determine the entrypoint
    # For a TypeScript MCP server, the entrypoint should be the built file
    entrypoint = "dist/index.js"
    agent_name = "mcp_server"  # Must use underscores, not hyphens
    
    print(f"\n3. Running agentcore configure...")
    print(f"   Entrypoint: {entrypoint}")
    print(f"   Agent name: {agent_name}")
    
    # Create the authorizer config JSON
    authorizer_config = {
        "oidcDiscoveryUrl": config['discovery_url'],
        "allowedAudiences": [config['client_id']],
        "allowedClients": [config['client_id']]
    }
    authorizer_config_str = json.dumps(authorizer_config)
    
    cmd = [
        'agentcore', 'configure',
        '--protocol', 'MCP',
        '--entrypoint', entrypoint,
        '--execution-role', config['role_arn'],
        '--authorizer-config', authorizer_config_str,
        '--name', agent_name,
        '--region', config['region']
    ]
    
    print(f"\n   Authorizer Config: {authorizer_config_str}")
    print(f"\n   Command: agentcore configure --protocol MCP --entrypoint {entrypoint} ...")
    print("\n" + "=" * 70)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("\n✅ Configuration successful!")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Configuration failed!")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("\nThis script will configure your MCP server with Bedrock Agentcore.")
    print("It will retrieve or create the necessary AWS resources.\n")
    
    # Get or create configuration
    config = get_or_create_configuration()
    
    if not config:
        print("\n❌ Failed to get configuration")
        sys.exit(1)
    
    # Run agentcore configure
    success = run_agentcore_configure(config)
    
    if success:
        print("\n" + "=" * 70)
        print("Next steps:")
        print("1. Build your TypeScript project: npm run build")
        print("2. Deploy your agent: agentcore deploy")
        print("=" * 70)
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
