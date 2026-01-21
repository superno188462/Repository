import requests
import os
import time
import json
from tool import nested_dict

dict = {
    # "新股":"data/new_stock/",
    # "股息率":"data/stock/dividend_rate/",
    # "套利股":"data/taoligu/",
    # "债券":"data/bond/",
    # "封闭基金":"data/cb/",
    # "ETF":"data/etf/",
    # "现金管理":"data/repo/",
    # "A/H比价":"data/ha/",
    # "T+0 QDII":"data/qdii/",
    # "REITs":"data/cnreits/",
    "LOF":{
        "股票LOF":"data/lof/stock_lof_list/",
        "指数LOF":"data/lof/index_lof_list/",
    },
}


# 对内接口
url_base = 'https://www.jisilu.cn/'
data_dir = "jisilu/data"
_session = None
def _get_session():
    global _session
    if _session == None:
        _session = requests.Session()
        _session.verify = False
        # _session.trust_env = False
    return _session

def _get_all_data():
    all_data = nested_dict()
    session = _get_session()
    for type1, tmp_dict in dict.items():
        for type2, url_path in tmp_dict.items():
            data_file_name = f"{data_dir}/{type2}.json"
            path = os.path.join(url_base, url_path)

            # 近期抓取过不重复抓取
            should_fetch = True
            if os.path.exists(data_file_name):
                file_mtime = os.path.getmtime(data_file_name)
                current_time = time.time()
                if current_time - file_mtime < 3600:
                    print(f"使用缓存文件: {data_file_name}")
                    should_fetch = False
            if should_fetch:
                response = session.post(path)
                with open(data_file_name, "w", encoding="utf-8") as f:
                    f.write(response.text)
                
             # 尝试读取数据文件
            with open(data_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data["rows"]:
                    item["cell"]["type"] = type2
                    all_data[item["id"]] = item["cell"]
    return all_data

# 对外接口
def get_all_data():
    return _get_all_data()




       
