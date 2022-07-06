import os
import json
import shutil
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))

    CVE_PATH = os.path.join(config.data_folder, config.dataset.cve_id)
    PROJ_PATH = os.path.join(CVE_PATH, config.dataset.project_name)
    DATA_FORMAT_FILENAME = os.path.join(config.data_folder, config.data_format_filename)

    with open(DATA_FORMAT_FILENAME, "r") as f:
        data_format = json.load(f)
    
    RESULTS_PATH = os.path.join(PROJ_PATH, data_format["files"]["results_path"])
    SELECT_RESULTS_PATH = os.path.join(PROJ_PATH, data_format["files"]["select_results_path"])
    
    MODEL_CVE_DATA_FOLDER = os.path.join(config.model_data_folder, config.dataset.cve_id)
    RESULTS_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, data_format["files"]["results_path"])
    
    model_folder_path = config.model_data_folder.replace("data", "")[:-1]
    MODEL_SELECT_RESULTS_PATH = os.path.join(model_folder_path, data_format["files"]["select_results_path"])

    shutil.copyfile(RESULTS_JSON_FILE_PATH, RESULTS_PATH)
    shutil.copyfile(MODEL_SELECT_RESULTS_PATH, SELECT_RESULTS_PATH)

    with open(SELECT_RESULTS_PATH, "r") as f:
        results = json.load(f)
    
    total_cnt = 0
    corr_cnt = 0
    incorr_cnt = 0
    for filename in results:
        print(f"File: {filename}:")
        for XFG, label, output in results[filename]:
            XFG.sort()
            if label == 1:
                total_cnt += 1
                if label == output:
                    corr_cnt += 1
                else:
                    print(f"XFG: {XFG}; Expected: {label} Evaluated to: {output}")
                    incorr_cnt += 1
    
    OUTPUT_TEXT_FILE_PATH = os.path.join(PROJ_PATH, data_format["files"]["stats_path"])

    with open(OUTPUT_TEXT_FILE_PATH, "w") as f:
        f.write(f"Correct guesses: {corr_cnt} / {total_cnt}\nAccuracy: {(corr_cnt / (total_cnt)) * 100}%")


if __name__ == "__main__":
    main()