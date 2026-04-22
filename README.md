# Hokmah MCP Server

**AI Agent with Architectural Memory — MCP Server**

Gives any AI coding agent persistent understanding of codebases via TransitionGraph, IdeaGraph, and WorldModel. Analyze impact, generate tests, write code — all from the graph.

<!-- mcp-name: io.github.davidangularme/hokmah -->

## Quick Start (30 seconds)

Add to your editor's MCP config (Cursor, Claude Code, VS Code, Windsurf, Cline, JetBrains):

```json
{
  "mcpServers": {
    "hokmah": {
      "type": "streamable-http",
      "url": "https://hokmah.dev/mcp"
    }
  }
}
```

Then ask your agent: *"analyze the impact of refactoring the auth module in github.com/owner/repo"*

## Available Tools

| Tool | Tier | Description |
|------|------|-------------|
| `hokmah_analyze` | **FREE** | Impact analysis, risk score, affected files, architectural invariants |
| `hokmah_connect_project` | **FREE** | Connect a GitHub repo, build the architectural graph |
| `hokmah_connect_mcp` | **FREE** | Connect an external MCP server for orchestration |
| `hokmah_generate_tests` | **PRO** | Test generation from the graph (40x fewer tokens) |
| `hokmah_generate_code` | **PRO** | Code generation with architectural memory |

## How It Works

Hokmah builds a persistent architectural graph from your codebase:

- **TransitionGraph** — Markov model of code changes (which files change together)
- **IdeaGraph** — 16 relation types between concepts
- **WorldModel** — File tree, dependencies, symbols

When you ask "what's the impact of changing X?", Hokmah traverses the graph instead of sending your entire codebase to an LLM. That's why `analyze` is free (zero LLM tokens) and `generate` uses 40x fewer tokens.

## Pricing

- **Free** — `hokmah_analyze` + `hokmah_connect_project` + `hokmah_connect_mcp` (unlimited)
- **Pro** — `hokmah_generate_tests` + `hokmah_generate_code` (BYOK — bring your own LLM key)

Get a Pro key at [hokmah.dev](https://hokmah.dev).

## Editor Setup

- **Cursor** — Settings → MCP → Add server → paste config
- **Claude Desktop** — `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Claude Code** — `claude mcp add hokmah --transport streamable-http --url https://hokmah.dev/mcp`
- **VS Code (Copilot)** — `.vscode/mcp.json` in project root
- **Windsurf** — `~/.windsurf/mcp.json`
- **Cline** — Settings → MCP Servers → Add
- **JetBrains** — Settings → Tools → AI Assistant → MCP Servers

## Self-Hosting

The hosted server at `https://hokmah.dev/mcp` is the recommended way to use Hokmah. To run the server yourself against your own Hokmah backend:

```bash
pip install -r requirements.txt
cp pro_keys.example.json pro_keys.json  # edit with your real PRO keys
HOKMAH_API_BASE=http://localhost:8000 python mcp_server.py
```

Environment variables:

- `HOKMAH_API_BASE` — upstream Hokmah API (default `http://localhost:8000`)
- `HOKMAH_MCP_PORT` — port to listen on (default `8001`)
- `HOKMAH_PRO_KEYS` — path to the PRO keys JSON file (default `/home/vpm/mcp-server/pro_keys.json`)

A reference `systemd` unit is provided in [`hokmah-mcp.service`](hokmah-mcp.service).

## Built by

[Catalyst AI Research](https://catalystais.com) · Haifa, Israel

## License

MIT
