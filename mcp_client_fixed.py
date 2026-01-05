"""
Fixed version of the Cognito setup code with proper error handling
Copy this code into your mcp_client.ipynb notebook
"""

# Cell 1: Import utilities
import sys
import os

# Get the current notebook's directory
current_dir = os.path.dirname(os.path.abspath('__file__' if '__file__' in globals() else '.'))

utils_dir = os.path.join(current_dir, '..')
utils_dir = os.path.abspath(utils_dir)

# Add to sys.path
sys.path.insert(0, utils_dir)
print("sys.path[0]:", sys.path[0])

from utils import create_agentcore_role, setup_cognito_user_pool

# Cell 2: Setup Cognito with proper error handling
print("Setting up Amazon Cognito user pool...")
cognito_config = setup_cognito_user_pool()

if cognito_config is None:
    print("❌ Cognito setup failed!")
    print("\nPossible reasons:")
    print("1. Missing IAM permissions (cognito-idp:* actions)")
    print("2. AWS credentials not configured")
    print("3. Network/connectivity issues")
    print("\nPlease check the error message above for details.")
else:
    print("Cognito setup completed ✓")
    print(f"User Pool ID: {cognito_config.get('pool_id', 'N/A')}")
    print(f"Client ID: {cognito_config.get('client_id', 'N/A')}")
    print(f"Discovery URL: {cognito_config.get('discovery_url', 'N/A')}")
    print(f"\nBearer Token (first 50 chars): {cognito_config.get('bearer_token', 'N/A')[:50]}...")
