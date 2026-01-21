from tool import load_config
_config = load_config("config.toml")
third_tool_config = _config["third_tool"]
config = _config["jisilu"]
print(config)

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from jisilu.jisilu_request import get_all_data
from third_tool import fangtang_message
from tool import nested_dict, pd_to_md, pd_rename_columns, pd_select_columns

class Jisilu:
    def __init__(self):
        self.data = {}
        self.update()

    def update(self):
        pass

    # 获取单个数据
    def get_data_by_id(self, id):
        data = get_all_data()[id]
        return data

    # 获取多个数据并分类
    def get_datas_by_ids(self, ids):
        datas = nested_dict()
        for id in ids:
            data = self.get_data_by_id(id)
            datas[data["type"]][id] = data
        return datas

    
    # 将分类数据转换成多个pd表
    def datas_to_pd(self, datas):
        if not datas: return {}
        
        # 定义每个类型要显示的字段（按优先级排序）
        field_mapping = {
            "指数LOF": [
                "fund_id", "fund_nm", "price", "increase_rt", "discount_rt",
                "fund_nav", "estimate_value", "index_nm", "index_increase_rt",
                "amount", "turnover_rt", "issuer_nm"
            ],
            "股票LOF": [
                "fund_id", "fund_nm", "price", "increase_rt", "discount_rt",
                "fund_nav", "estimate_value", "stock_ratio", "stock_increase_rt",
                "amount", "turnover_rt", "issuer_nm"
            ],
        }
        
        # 字段中文名称映射
        field_names = {
            "fund_id": "基金代码",
            "fund_nm": "基金名称",
            "price": "现价",
            "increase_rt": "涨跌幅(%)",
            "discount_rt": "溢价率(%)",
            "fund_nav": "基金净值",
            "estimate_value": "估算净值",
            "index_nm": "跟踪指数",
            "index_increase_rt": "指数涨跌(%)",
            "stock_ratio": "股票占比(%)",
            "stock_increase_rt": "股票涨跌(%)",
            "amount": "份额(万份)",
            "turnover_rt": "换手率(%)",
            "issuer_nm": "基金公司",
            "asset_ratio": "资产占比(%)",
            "pre_close": "昨收",
            "volume": "成交量",
            "price_dt": "价格日期",
            "nav_dt": "净值日期",
            "apply_status": "申购状态",
            "redeem_status": "赎回状态",
        }
        
        result = {}
        for classify_type, classify_data in datas.items():
            if not classify_data:
                continue
            # 步骤1: dict转pd
            df = pd.DataFrame(list(classify_data.values()))
            if df.empty: continue
            df = pd_select_columns(df, field_mapping[classify_type])
            df = pd_rename_columns(df, field_names)
            
            if df.empty:
                continue
            result[classify_type] = df
        return result
    
    
    
    def md(self, datas):
        if not datas: return ""
        
        # 转换为DataFrame
        dfs = self.datas_to_pd(datas)
        
        if isinstance(dfs, dict):
            # 多个DataFrame，生成多个表格
            md_tables = []
            for ft, df in dfs.items():
                table = pd_to_md(df, ft)
                if table:
                    md_tables.append(table)
            return "\n".join(md_tables)
    

def get_datas_by_ids_message_from_fangtang():
    jisilu = Jisilu()
    datas = jisilu.get_datas_by_ids(config["list"])
    md = jisilu.md(datas)
    fangtang_message(third_tool_config["fangtang_api_key"], "LOF-溢价", md)


if __name__ == "__main__":
    get_datas_by_ids_message_from_fangtang()
