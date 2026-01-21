import tomllib
def load_config(path="config.toml"): return tomllib.load(open(path, "rb"))

from collections import defaultdict
def nested_dict(): return defaultdict(nested_dict)


# pandas相关工具
import pandas as pd
# 将pd转换为表格形式的md，方便进行文本传输
def pd_to_md(df, title=None):
        if df is None or df.empty:
            return ""
        
        md_lines = []
        
        # 添加标题
        if title:
            md_lines.append(f"## {title}\n")
        
        # 计算每列的最大宽度（包括表头）
        column_widths = {}
        for col in df.columns:
            # 表头宽度
            header_width = len(str(col))
            # 数据列的最大宽度
            data_width = df[col].astype(str).str.len().max() if not df[col].empty else 0
            # 取较大值，并添加一些padding
            column_widths[col] = max(header_width, data_width) + 1
        
        # 格式化函数：将值格式化为指定宽度
        def format_cell(value, width):
            value_str = str(value) if value is not None and str(value) != 'nan' else '-'
            return value_str.ljust(width)
        
        # 生成表头
        header_cells = [format_cell(col, column_widths[col]) for col in df.columns]
        header_row = "| " + " | ".join(header_cells) + " |"
        md_lines.append(header_row)
        
        # 生成分隔行（对齐标记）
        separator_cells = ["-" * column_widths[col] for col in df.columns]
        separator_row = "| " + " | ".join(separator_cells) + " |"
        md_lines.append(separator_row)
        
        # 生成数据行
        for _, row in df.iterrows():
            row_cells = [format_cell(row[col], column_widths[col]) for col in df.columns]
            data_row = "| " + " | ".join(row_cells) + " |"
            md_lines.append(data_row)
        
        md_lines.append("")  # 添加空行
        return "\n".join(md_lines)
    
# 重命名列名 field_names 字典映射关系
def pd_rename_columns(df, field_names): 
    column_mapping = {col: field_names.get(col, col) for col in df.columns}
    return df.rename(columns=column_mapping)

def pd_select_columns(df, keep_list):
        available_fields = [f for f in keep_list if f in df.columns]
        if not available_fields:
            return pd.DataFrame()
        return df[available_fields]
    
    
