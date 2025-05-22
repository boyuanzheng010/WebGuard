from datasets import Dataset, DatasetDict
import pandas as pd
from huggingface_hub import HfApi

# Step 1: 读取 JSON 文件
file_path = "data/all_reviewed_annotation_4_15.json"
df = pd.read_json(file_path)

"""
    {
        "action_id": 5,
        "url": "https://www.spotify.com/us/download/windows/",
        "description": NaN,
        "tagHead": "a",
        "Screenshot": NaN,
        "Screenshot View": "https://drive.google.com/file/d/1DBlK-rPnGaGb55ghoc2leYhQQwlaofZD/view?usp=drivesdk",
        "Annotation": "HIGH",
        "Your Review": "HIGH",
        "folder_name": "downloads/SPOTIFY",
        "folder": "annot_batch_Windows_download_-_Spotify_id_c536a5a9-ee2e-499b-a206-f78971746c2a_from_www_spotify_com_us_download_wi",
        "annotation_folder": "annot_HIGH_Tgt_Download_directly_from_Spotify_d84adba7-d41f-414b-9ab9-7b1ee7a6f18b",
        "Reason": NaN,
        "website": "SPOTIFY"
    },
"""

# # 可选：删除含 NaN 的列或行（否则上传可能报错）
# df = df.dropna(axis=1, how='all')  # 删除全是 NaN 的列
# df = df.dropna(subset=['action_id', "url", 'description', "Annotation", "Your Review"])  # 保留主要字段

# Step 2: 转换为 HuggingFace 的 Dataset 对象
dataset = Dataset.from_pandas(df)

# Step 3: 上传到 Hugging Face Hub
dataset.push_to_hub("boyuanzheng010/webguard")