# Postman Setup Guide for MCP Server

## Quick Setup

### 1. List All Tools

**Method:** `POST`  
**URL:** `http://localhost:3001/mcp`

**Headers:**
```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**Body (raw JSON):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/list",
  "id": 1
}
```

---

### 2. Call Add Tool

**Method:** `POST`  
**URL:** `http://localhost:3001/mcp`

**Headers:**
```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**Body (raw JSON):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "add",
    "arguments": {
      "a": 5,
      "b": 3
    }
  },
  "id": 2
}
```

**Expected Response:**
```json
{
  "result": {
    "content": [
      {
        "type": "text",
        "text": "8"
      }
    ]
  },
  "jsonrpc": "2.0",
  "id": 2
}
```

---

### 3. Call Subtract Tool

**Method:** `POST`  
**URL:** `http://localhost:3001/mcp`

**Headers:**
```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**Body (raw JSON):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "subtract",
    "arguments": {
      "a": 10,
      "b": 4
    }
  },
  "id": 3
}
```

---

### 4. Call Greeting Tool

**Method:** `POST`  
**URL:** `http://localhost:3001/mcp`

**Headers:**
```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**Body (raw JSON):**
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "greetingPrompt",
    "arguments": {
      "name": "John"
    }
  },
  "id": 4
}
```

---

## Step-by-Step in Postman

### Creating a New Request

1. **Open Postman** and click "New" → "HTTP Request"

2. **Set the Method and URL:**
   - Method: `POST`
   - URL: `http://localhost:3001/mcp`

3. **Configure Headers:**
   - Click the "Headers" tab
   - Add two headers:
     - Key: `Content-Type`, Value: `application/json`
     - Key: `Accept`, Value: `application/json, text/event-stream`

4. **Configure Body:**
   - Click the "Body" tab
   - Select "raw"
   - Choose "JSON" from the dropdown (on the right)
   - Paste one of the JSON examples above

5. **Click Send**

---

## ⚠️ Critical Notes

1. **The Accept header is REQUIRED** - Without `Accept: application/json, text/event-stream`, you'll get the error:
   ```json
   {
     "jsonrpc": "2.0",
     "error": {
       "code": -32000,
       "message": "Not Acceptable: Client must accept both application/json and text/event-stream"
     },
     "id": null
   }
   ```

2. **Make sure your server is running:**
   ```bash
   npm run start
   ```

3. **The server should be listening on port 3001**

---

## Importing as Postman Collection

You can also import the `postman_collection.json` file (see next section) directly into Postman:

1. Click "Import" in Postman
2. Select the `postman_collection.json` file
3. All requests will be pre-configured
