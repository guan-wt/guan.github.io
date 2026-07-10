import requests
import json

# ========== 替换成你自己的信息 ==========
APP_ID = "你的AppID"
APP_SECRET = "你的AppSecret"
BITABLE_APP_TOKEN = "多维表格app_token"
BITABLE_TABLE_ID = "数据表table_id"
# 多维表格内字段名（和你表格一致）
FIELD_NAME = "影视名称"
FIELD_TYPE = "分类"
# =======================================

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
        items = res.json()["data"]["items"]
        for item in items:
            fields = item["fields"]
            name = fields.get(FIELD_NAME, "")
            typ = fields.get(FIELD_TYPE, "")
            if name:
                all_data.append({"name": name, "type": typ})
        page_token = res.json()["data"].get("page_token")
        if not page_token:
            break
    return all_data

if __name__ == "__main__":
    data = get_all_records()
    # 生成data.json放到网站根目录
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("数据已导出到 data.json")
