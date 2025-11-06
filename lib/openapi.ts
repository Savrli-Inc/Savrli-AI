export const openapiSpec = {
  openapi: "3.0.3",
  info: {
    title: "Savrli AI API",
    version: "1.0.0",
    description: "Endpoints for Quick Ask Kai"
  },
  servers: [{ url: "https://savrli-ai.vercel.app" }],
  paths: {
    "/api/ai/chat": {
      post: {
        summary: "Chat with Kai",
        requestBody: {
          required: true,
          content: {
            "application/json": {
              schema: {
                type: "object",
                properties: {
                  messages: {
                    type: "array",
                    items: {
                      type: "object",
                      properties: {
                        role: { type: "string", enum: ["user","system","assistant"] },
                        content: { type: "string" }
                      },
                      required: ["role","content"]
                    }
                  }
                },
                required: ["messages"]
              },
              example: {
                messages: [{ role: "user", content: "Hello Kai" }]
              }
            }
          }
        },
        responses: {
          "200": {
            description: "Chat response",
            content: {
              "application/json": {
                schema: {
                  type: "object",
                  properties: {
                    ok: { type: "boolean" },
                    reply: { type: "string" }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
} as const;
