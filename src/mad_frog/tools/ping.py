import json

BMAD_PING_TOOL = {
    "name": "bmad_ping",
    "description": "Health check — returns server status and version.",
    "inputSchema": {
        "type": "object",
        "properties": {},
    },
}


def handle_bmad_ping() -> dict:
    result_data = {"status": "ok", "version": "0.1.0"}
    return {
        "content": [{"type": "text", "text": json.dumps(result_data)}],
        "isError": False,
    }
