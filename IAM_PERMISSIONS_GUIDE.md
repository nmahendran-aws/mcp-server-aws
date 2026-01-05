# Complete IAM Permissions Guide for utils.py

This document lists ALL IAM permissions required for the `aiengineer` user to run the functions in `utils.py`.

## Summary

You need permissions for:
1. **Cognito User Pool Management** (for `setup_cognito_user_pool()`)
2. **IAM Role Management** (for `create_agentcore_role()`)
3. **STS** (for getting account ID)

## Complete IAM Policy

Copy this entire policy and attach it to your `aiengineer` IAM user:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "CognitoUserPoolManagement",
      "Effect": "Allow",
      "Action": [
        "cognito-idp:CreateUserPool",
        "cognito-idp:CreateUserPoolClient",
        "cognito-idp:AdminCreateUser",
        "cognito-idp:AdminSetUserPassword",
        "cognito-idp:InitiateAuth"
      ],
      "Resource": "*"
    },
    {
      "Sid": "IAMRoleManagement",
      "Effect": "Allow",
      "Action": [
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy",
        "iam:ListRolePolicies",
        "iam:GetRole"
      ],
      "Resource": "arn:aws:iam::*:role/agentcore-*"
    },
    {
      "Sid": "STSGetCallerIdentity",
      "Effect": "Allow",
      "Action": [
        "sts:GetCallerIdentity"
      ],
      "Resource": "*"
    }
  ]
}
```

## Breakdown by Function

### 1. `setup_cognito_user_pool()`
**Cognito Permissions Required:**
- `cognito-idp:CreateUserPool` - Create the user pool
- `cognito-idp:CreateUserPoolClient` - Create app client
- `cognito-idp:AdminCreateUser` - Create the test user
- `cognito-idp:AdminSetUserPassword` - Set permanent password
- `cognito-idp:InitiateAuth` - Authenticate and get tokens

### 2. `create_agentcore_role()`
**IAM Permissions Required:**
- `iam:CreateRole` - Create IAM role for agentcore
- `iam:DeleteRole` - Delete role if it already exists
- `iam:PutRolePolicy` - Attach inline policy to role
- `iam:DeleteRolePolicy` - Delete policy from role
- `iam:ListRolePolicies` - List policies on role
- `iam:GetRole` - Check if role exists

**STS Permissions Required:**
- `sts:GetCallerIdentity` - Get AWS account ID

## How to Apply This Policy

### Option 1: AWS Console (Recommended)

1. Go to **IAM Console** → **Users** → `aiengineer`
2. Click **Add permissions** → **Create inline policy**
3. Click **JSON** tab
4. Paste the complete policy above
5. Click **Review policy**
6. Name it: `MCPUtilsPolicy`
7. Click **Create policy**

### Option 2: AWS CLI

```bash
aws iam put-user-policy \
  --user-name aiengineer \
  --policy-name MCPUtilsPolicy \
  --policy-document file://iam-policy-complete.json
```

## Security Notes

- The IAM role permissions are scoped to only roles starting with `agentcore-*`
- Cognito and STS permissions require `Resource: "*"` as they don't support resource-level permissions
- This policy follows the principle of least privilege for the operations in `utils.py`

## Files

- `iam-policy-complete.json` - The policy in JSON format ready to use
- This guide

## Testing

After applying the policy, re-run your notebook. Both functions should work without permission errors.
