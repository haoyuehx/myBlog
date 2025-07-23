import requests
import json
import os

def fetch_bangumi_data():
    url = "https://api.bgm.tv/v0/users/1024520/collections?subject_type=2&type=2&limit=30&offset=0"
    headers = {"accept": "application/json", "User-Agent": "MyHugoBlog/1.0 (https://yourblog.com)"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        # 确保data目录存在
        os.makedirs("data", exist_ok=True)
        
        # 保存数据
        with open("data/bangumi.json", "w", encoding="utf-8") as f:
            json.dump(data["data"], f, ensure_ascii=False, indent=2)
        print("Bangumi数据获取成功！")
    except Exception as e:
        print(f"获取Bangumi数据失败: {e}")

if __name__ == "__main__":
    fetch_bangumi_data()