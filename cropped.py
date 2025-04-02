import os
import sys
import json
import configparser
from PIL import Image


config_file_name = 'config.ini'

# get root 
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)     

# get setting
CONFIG_PATH = os.path.join(application_path, config_file_name)
config = configparser.ConfigParser()
config.read(CONFIG_PATH,encoding="utf-8")

# 載入 JSON 檔案
json_file_path = config['system']['source_path']
output_folder = r"cropped_images"

# 確保輸出資料夾存在
os.makedirs(output_folder, exist_ok=True)

# 開啟 JSON 檔案
with open(json_file_path, 'r') as f:
    data = json.load(f)

# 處理每個檔案
for prediction in data["predictions"]:
 
    image_path = prediction["filepath"].replace("/", os.sep)
    
    # 確認影像檔案是否存在
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        continue

    # 開啟影像
    image = Image.open(image_path)
    image_width, image_height = image.size

    # 處理每個檢測框
    for i, detection in enumerate(prediction["detections"]):
        bbox = detection["bbox"]
        conf = detection["conf"]

        # 只處理 conf > 0.5 的檢測框
        if conf <= 0.5:
            continue

        # 計算實際像素座標
        left = int(bbox[0] * image_width)
        top = int(bbox[1] * image_height)
        right = int((bbox[0] + bbox[2]) * image_width)
        bottom = int((bbox[1] + bbox[3]) * image_height)

        # 裁切影像
        cropped_image = image.crop((left, top, right, bottom))

        # 儲存裁切後的影像
        output_path = os.path.join(
            output_folder,
            f"{os.path.splitext(os.path.basename(prediction['filepath']))[0]}_crop_{i + 1}.jpg"
        )
        cropped_image.save(output_path)
        print(f"Saved cropped image: {output_path}")