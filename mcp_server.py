import os
import json
import httpx
from fastmcp import FastMCP

API_BASE = os.getenv("HOKMAH_API_BASE", "http://localhost:8000")
MCP_PORT = int(os.getenv("HOKMAH_MCP_PORT", "8001"))
PRO_KEYS_FILE = os.getenv("HOKMAH_PRO_KEYS", "/home/vpm/mcp-server/pro_keys.json")


def _check_pro_key(api_key: str) -> bool:
    try:
        with open(PRO_KEYS_FILE) as f:
            return api_key in set(json.load(f).get("keys", []))
    except Exception:
        return False


def _project_id_from_repo(repo_url: str) -> str:
    """Derive a stable project_id from a GitHub URL: github.com/owner/name -> owner/name."""
    s = repo_url.rstrip("/")
    if s.endswith(".git"):
        s = s[:-4]
    parts = s.split("/")
    if len(parts) >= 2:
        return f"{parts[-2]}/{parts[-1]}"
    return s


async def _post(endpoint: str, payload: dict, timeout: float = 120.0) -> dict:
    async with httpx.AsyncClient(base_url=API_BASE, timeout=timeout) as c:
        r = await c.post(endpoint, json=payload)
        r.raise_for_status()
        return r.json()


def _execute_payload(
    repo_url: str,
    query: str,
    mode: str,
    branch: str,
    tenant_id: str = "default",
) -> dict:
    return {
        "tenant_id": tenant_id,
        "project_id": _project_id_from_repo(repo_url),
        "instruction": query,
        "mode": mode,
    }


mcp = FastMCP(
    name="hokmah",
    instructions=(
        "Hokmah — AI Agent with Architectural Memory. "
        "Gives any AI coding agent persistent codebase understanding. "
        "analyze=FREE, generate=PRO."
    ),
)


@mcp.tool()
async def hokmah_analyze(repo_url: str, query: str, branch: str = "main") -> dict:
    """Analyze impact of a code change. Returns risk score, affected files, invariants. FREE — zero LLM tokens."""
    return await _post("/v2/execute", _execute_payload(repo_url, query, "analyze", branch))


@mcp.tool()
async def hokmah_generate_tests(
    repo_url: str, query: str, api_key: str, branch: str = "main"
) -> dict:
    """Generate tests from the architectural graph. 40x fewer tokens. PRO — requires API key."""
    if not _check_pro_key(api_key):
        return {"error": "Invalid or missing PRO API key. Get one at https://hokmah.dev"}
    return await _post("/v2/execute", _execute_payload(repo_url, query, "test", branch))


@mcp.tool()
async def hokmah_generate_code(
    repo_url: str, query: str, api_key: str, branch: str = "main"
) -> dict:
    """Generate code with architectural memory. Reduces hallucination via graph context. PRO — requires API key."""
    if not _check_pro_key(api_key):
        return {"error": "Invalid or missing PRO API key. Get one at https://hokmah.dev"}
    return await _post("/v2/execute", _execute_payload(repo_url, query, "code", branch))


@mcp.tool()
async def hokmah_connect_project(repo_url: str, branch: str = "main") -> dict:
    """Connect a GitHub repo to Hokmah. Builds TransitionGraph + IdeaGraph + WorldModel from commit history. FREE."""
    return await _post(
        "/v2/execute",
        _execute_payload(repo_url, "initial connection", "analyze", branch),
    )


@mcp.tool()
async def hokmah_connect_mcp(
    server_url: str,
    server_name: str,
    tenant: str = "default",
    project: str = "default",
) -> dict:
    """Connect an external MCP server to Hokmah for universal tool orchestration. FREE."""
    return await _post(
        "/mcp/connect",
        {
            "tenant_id": tenant,
            "project_id": project,
            "server_id": server_name,
            "url": server_url,
            "name": server_name,
        },
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=MCP_PORT)
