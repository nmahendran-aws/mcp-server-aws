// Test client for MCP Server
// This shows the correct way to make requests to the MCP server

async function testMCPServer() {
    const url = 'http://localhost:3001/mcp';

    // Example 1: List available tools
    const listToolsRequest = {
        jsonrpc: "2.0",
        method: "tools/list",
        id: 1
    };

    console.log('Testing tools/list endpoint...');

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // CRITICAL: Both Accept types are required
                'Accept': 'application/json, text/event-stream'
            },
            body: JSON.stringify(listToolsRequest)
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Error response:', errorText);
            return;
        }

        const data = await response.json();
        console.log('Success! Available tools:', JSON.stringify(data, null, 2));

        // Example 2: Call the add tool
        console.log('\nTesting add tool...');
        const addRequest = {
            jsonrpc: "2.0",
            method: "tools/call",
            params: {
                name: "add",
                arguments: {
                    a: 5,
                    b: 3
                }
            },
            id: 2
        };

        const addResponse = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json, text/event-stream'
            },
            body: JSON.stringify(addRequest)
        });

        const addData = await addResponse.json();
        console.log('Add result:', JSON.stringify(addData, null, 2));

    } catch (error) {
        console.error('Request failed:', error);
    }
}

// Run the test
testMCPServer();
