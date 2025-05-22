import requests

url = "https://huggingface.co/api/datasets/boyuanzheng010/webguard/croissant"
response = requests.get(url)
croissant_metadata = response.json()

# 将元数据保存到文件
with open("webguard_croissant.json", "w", encoding="utf-8") as f:
    import json
    json.dump(croissant_metadata, f, ensure_ascii=False, indent=2)