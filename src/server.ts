import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export const mcpServerCreate = () => {
    const mcpServer = new McpServer({
        name: "MCP Server",
        description: "MCP Server",
        version: "1.0.0",
    });

    mcpServer.registerTool("add",
        {
            title: "Add",
            description: "Add two numbers",
            inputSchema: { a: z.number(), b: z.number() }
        },
        async ({ a, b }) => ({
            content: [{ type: "text", text: `${a + b}` }]
        })
    );

    mcpServer.registerTool("subtract",
        {
            title: "Subtract",
            description: "Subtract two numbers",
            inputSchema: { a: z.number(), b: z.number() }
        },
        async ({ a, b }) => ({
            content: [{ type: "text", text: `${a - b}` }]
        })
    );

    mcpServer.registerTool("greetingPrompt",
        {
            title: "Greeting Prompt",
            description: "Generate a personalized greeting",
            inputSchema: { name: z.string() }
        },
        async ({ name }) => ({
            content: [{ type: "text", text: `Hello, ${name}! Welcome to MCP Server.` }]
        })
    );

    return mcpServer;
}
