import requests
import json
import os

# ========== 字段名保持不变，不要动 ==========
FIELD_NAME = "名称"
FIELD_YEAR = "年份"
FIELD_TYPE = "类型"
FIELD_QUARK = "夸克"
FIELD_SIZE = "格式大小"
FIELD_SUB = "语言字幕"
FIELD_CLEAR = "清晰度"
FIELD_TAG = "标签"
# =======================================

# 从GitHub Actions环境变量读取，不写死密钥
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
BITABLE_APP_TOKEN = os.getenv("BITABLE_APP_TOKEN")
BITABLE_TABLE_ID = os.getenv("BITABLE_TABLE_ID")

def get_tenant_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    return resp.json()["tenant_access_token"]

def get_all_records():
    token = get_tenant_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{BITABLE_APP_TOKEN}/tables/{BITABLE_TABLE_ID}/records/search"
    all_data = []
    page_token = ""
    while True:
        payload = {"page_size": 100}
        if page_token:
            payload["page_token"] = page_token
        res = requests.post(url, headers=headers, json=payload)
        resp_data = res.json()
        items = resp_data["data"]["items"]
        for item in items:
            f = item["fields"]
            row = {
                "name": f.get(FIELD_NAME, ""),
                "year": f.get(FIELD_YEAR, ""),
                "type": f.get(FIELD_TYPE, ""),
                "quark": f.get(FIELD_QUARK, ""),
                "size": f.get(FIELD_SIZE, ""),
                "sub": f.get(FIELD_SUB, ""),
                "clear": f.get(FIELD_CLEAR, ""),
                "tag": f.get(FIELD_TAG, "")
            }
            if row["name"]:
                all_data.append(row)
        page_token = resp_data["data"].get("page_token")
        if not page_token:
            break
    return all_data

if __name__ == "__main__":
    data = get_all_records()
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("导出完成 data.json")
