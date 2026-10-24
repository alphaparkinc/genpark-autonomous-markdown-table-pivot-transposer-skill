import sys, json
from client import AutonomousMarkdownTablePivotTransposerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    client = AutonomousMarkdownTablePivotTransposerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-autonomous-markdown-table-pivot-transposer-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    md = req.get("table", "")
    r = req.get("row_dim", "Region")
    c = req.get("col_dim", "Quarter")
    v = req.get("val_dim", "Revenue")
    res = client.pivot_table(md, r, c, v)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()
