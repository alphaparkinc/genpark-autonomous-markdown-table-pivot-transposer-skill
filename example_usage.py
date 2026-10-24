from client import AutonomousMarkdownTablePivotTransposerClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    client = AutonomousMarkdownTablePivotTransposerClient()
    print("=== AUTONOMOUS MARKDOWN TABLE PIVOT TRANSPOSER ===")
    
    input_md = """
| Region | Quarter | Revenue |
|---|---|---|
| North America | Q1 | $12000 |
| North America | Q2 | $15500 |
| Europe | Q1 | $8200 |
| Europe | Q2 | $9400 |
| Asia Pacific | Q1 | $11000 |
| Asia Pacific | Q2 | $13800 |
"""
    res = client.pivot_table(input_md, row_dim="Region", col_dim="Quarter", val_dim="Revenue", agg_fn="SUM")
    print(f"Pivot Aggregation: {res['aggregation']}({res['value_dimension']}) by {res['row_dimension']} x {res['column_dimension']}:")
    print()
    print(res['pivoted_markdown_table'])

if __name__ == "__main__":
    main()
