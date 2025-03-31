import os
import sys
import json
import shutil
import configparser

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


BLANK_SCORE_GATE = float(config['score']['BLANK_SCORE_GATE'])
PREDICTION_SCORE_GATE= float(config['score']['PREDICTION_SCORE_GATE'])
SOURCE_PATH = config['system']['source_path']
OUT_PATH = config['system']['out_path']


def organize_images(json_file, image_folder, output_folder):

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    os.makedirs(output_folder, exist_ok=True)

    for prediction in data["predictions"]:
        filepath = prediction["filepath"]
        prediction_score = prediction["prediction_score"]
        prediction_label = prediction["prediction"].split(";")[-1].strip()

        if prediction_label == "blank" and prediction_score >= BLANK_SCORE_GATE:
            target_folder = os.path.join(output_folder, "blank")
        elif prediction_label != "blank" and prediction_score >= PREDICTION_SCORE_GATE:
            target_folder = os.path.join(output_folder, prediction_label)
        else:
            target_folder = os.path.join(output_folder, "others")

        os.makedirs(target_folder, exist_ok=True)

        source_path = os.path.join(image_folder, os.path.basename(filepath))
        filename, ext = os.path.splitext(os.path.basename(filepath))
        new_filename = f"{filename}_{prediction_score:.2f}{ext}"
        target_path = os.path.join(target_folder, new_filename)
        
        if os.path.exists(source_path):
            shutil.copy(source_path, target_path)
            print(f"Copied {source_path} to {target_path}")
        else:
            print(f"File not found: {source_path}")


json_file = SOURCE_PATH
image_folder = "image"
output_folder = OUT_PATH

organize_images(json_file, image_folder, output_folder)