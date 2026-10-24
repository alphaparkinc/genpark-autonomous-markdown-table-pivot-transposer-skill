import re, sys
sys.stdout.reconfigure(encoding='utf-8')

class AutonomousMarkdownTablePivotTransposerClient:
    """
    Parses Markdown tables into structured matrices, performs cross-tabulation pivoting,
    applies aggregate calculations (SUM, AVG, COUNT, MAX), and emits cleanly formatted Markdown tables.
    """
    def __init__(self):
        pass

    def parse_markdown_table(self, md_table):
        lines = [line.strip() for line in md_table.strip().splitlines() if line.strip()]
        if len(lines) < 2:
            raise ValueError("Markdown table must contain at least a header and separator line")

        # Extract headers
        headers = [h.strip() for h in lines[0].strip('|').split('|')]
        rows = []
        for line in lines[2:]: # skip separator
            cells = [c.strip() for c in line.strip('|').split('|')]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
        return headers, rows

    def parse_numeric(self, val_str):
        clean = re.sub(r'[^0-9.-]', '', val_str)
        try:
            return float(clean)
        except ValueError:
            return 0.0

    def pivot_table(self, md_table, row_dim, col_dim, val_dim, agg_fn="SUM"):
        headers, rows = self.parse_markdown_table(md_table)
        if row_dim not in headers or col_dim not in headers or val_dim not in headers:
            raise ValueError(f"Specified dimensions must be in table headers: {headers}")

        unique_row_keys = sorted(list(set(r[row_dim] for r in rows)))
        unique_col_keys = sorted(list(set(r[col_dim] for r in rows)))

        # Group values
        grid = {r_k: {c_k: [] for c_k in unique_col_keys} for r_k in unique_row_keys}
        for r in rows:
            r_k = r[row_dim]
            c_k = r[col_dim]
            num = self.parse_numeric(r[val_dim])
            grid[r_k][c_k].append(num)

        # Aggregate values
        def compute_agg(nums):
            if not nums:
                return 0.0
            if agg_fn.upper() == "SUM":
                return sum(nums)
            elif agg_fn.upper() == "AVG":
                return sum(nums) / len(nums)
            elif agg_fn.upper() == "COUNT":
                return float(len(nums))
            elif agg_fn.upper() == "MAX":
                return max(nums)
            return sum(nums)

        pivot_data = []
        for r_k in unique_row_keys:
            row_dict = {row_dim: r_k}
            row_total = 0.0
            for c_k in unique_col_keys:
                agg_val = compute_agg(grid[r_k][c_k])
                row_dict[c_k] = round(agg_val, 2)
                row_total += agg_val
            row_dict["Total"] = round(row_total, 2)
            pivot_data.append(row_dict)

        # Build output markdown table
        out_headers = [row_dim] + unique_col_keys + ["Total"]
        header_line = "| " + " | ".join(out_headers) + " |"
        sep_line = "| " + " | ".join([":---"] + ["---:"] * (len(out_headers) - 1)) + " |"
        body_lines = []
        for item in pivot_data:
            vals = [str(item[h]) for h in out_headers]
            body_lines.append("| " + " | ".join(vals) + " |")

        formatted_md = "\n".join([header_line, sep_line] + body_lines)
        return {
            "status": "success",
            "row_dimension": row_dim,
            "column_dimension": col_dim,
            "value_dimension": val_dim,
            "aggregation": agg_fn.upper(),
            "output_rows_count": len(pivot_data),
            "pivoted_markdown_table": formatted_md
        }
