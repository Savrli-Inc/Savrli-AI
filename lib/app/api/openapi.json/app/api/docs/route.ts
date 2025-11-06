// app/api/docs/route.ts
import { NextResponse } from "next/server";

export const dynamic = "force-static";

const html = `<!doctype html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title>Savrli AI – API Docs</title>
    <link rel="stylesheet"
      href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
    <style>body { margin:0 } .topbar { display:none }</style>
  </head>
  <body>
    <div id="swagger"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      window.ui = SwaggerUIBundle({
        url: '/api/openapi.json',
        dom_id: '#swagger',
        presets: [SwaggerUIBundle.presets.apis],
        layout: "BaseLayout"
      });
    </script>
  </body>
</html>`;

export async function GET() {
  return new NextResponse(html, {
    headers: { "content-type": "text/html; charset=utf-8" }
  });
}
