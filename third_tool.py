from enum import verify
from tool import load_config
config = load_config("config.toml")["third_tool"]

import requests


# 可以把信息通过方糖服务号API传到微信等平台
def fangtang_message(apiKey, title, content, session=requests.Session()):
    data = {"text":title,"desp":content}
    msg_url = "https://sc.ftqq.com/{}.send".format(apiKey)
    session.post(msg_url, data=data, verify=False)
    # msg_url = "https://sc.ftqq.com/{}.send?text={}&desp={}".format(apiKey, title, content)
    # session.get(msg_url)

if __name__ == "__main__":
    fangtang_message(config["fangtang_api_key"],"测试","这是一条测试消息")
