import os
import sys
import json
import configparser
from PIL import Image

class Ctr_Image:
    def __init__(self, config_file_name='config.ini'):

        self.application_path = os.path.dirname(os.path.abspath(sys.argv[0]))

        self.config_file_name = config_file_name
        self.config_path = os.path.join(self.application_path, self.config_file_name)

        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        self.config = configparser.ConfigParser()
        self.config.read(self.config_path, encoding="utf-8")

        self.json_file_path = self.config['system']['source_path']
        self.output_folder = self.config['system']['out_path']
        
        os.makedirs(self.output_folder, exist_ok=True)

    def crop_images(self):
        # 開啟 JSON 檔案
        with open(self.json_file_path, 'r') as f:
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
                    self.output_folder,
                    f"{os.path.splitext(os.path.basename(prediction['filepath']))[0]}_crop_{i + 1}.jpg"
                )
                cropped_image.save(output_path)
                print(f"Saved cropped image: {output_path}")