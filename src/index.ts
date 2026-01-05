// MCP Server Entry Point
import { mcpServerCreate } from "./server";
import express, { Request, Response } from "express";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const port = 3001;
const app = express();
app.use(express.json());

const mcpServer = mcpServerCreate();
console.log('MCP Server initialized');

// Middleware to ensure Accept header is set correctly for MCP
app.use("/mcp", (req, res, next) => {
    const accept = req.get('Accept') || '';
    const required = ['application/json', 'text/event-stream'];
    const hasAll = required.every(type => accept.includes(type));

    if (!hasAll) {
        req.headers.accept = 'application/json, text/event-stream';
    }
    next();
});

app.post("/mcp", async (req: Request, res: Response) => {
    const server = mcpServerCreate();
    try {
        const transport: StreamableHTTPServerTransport = new StreamableHTTPServerTransport({
            sessionIdGenerator: undefined,
            enableJsonResponse: true
        });
        await server.connect(transport)
        await transport.handleRequest(req, res, req.body);
        res.on('close', () => {
            console.log('Client disconnected');
            transport.close();
            server.close();
        });
    } catch (error) {
        console.error(error);
        res.status(500).send("Internal Server Error");
    }
});

app.listen(port, "0.0.0.0", () => {
    console.log(`MCP Server listening on port ${port}`);
});
