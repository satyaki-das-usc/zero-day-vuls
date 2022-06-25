from genericpath import isdir, isfile
import os
import json
import shutil
from typing import cast
from importlib_metadata import files
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))
    
    CVE_PATH = os.path.join(config.data_folder, config.dataset.cve_id)
    PROJ_PATH = os.path.join(CVE_PATH, config.dataset.project_name)
    FIXED_HEADER_FOLDER = os.path.join(PROJ_PATH, config.fixed_header_folder)
    GROUND_TRUTH_PATH = os.path.join(PROJ_PATH, config.ground_truth_path)
    MODEL_DATA_FOLDER = config.model_data_folder
    MODEL_CVE_DATA_FOLDER = os.path.join(MODEL_DATA_FOLDER, config.dataset.cve_id)

    ALL_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "all.json")
    RESULTS_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "results.json")
    DONE_TXT_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "done.txt")
    CSV_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "csv")
    XFG_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "XFG")
    SOURCE_CODE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "source-code")

    files = [ALL_JSON_FILE_PATH, RESULTS_JSON_FILE_PATH, DONE_TXT_FILE_PATH]

    for filename in files:
        if os.path.isfile(filename):
            command = f"rm {filename}"
            os.system(command)
    
    folders = [CSV_PATH, XFG_PATH]

    for foldername in folders:
        if os.path.isdir(foldername):
            command = f"rm -rf {foldername}"
            os.system(command)
    
    rm_str = os.path.join(SOURCE_CODE_PATH, "*")
    command = f"rm {rm_str}"
    os.system(command)

    ground_truth_file = open(GROUND_TRUTH_PATH)
    ground_truth = json.load(ground_truth_file)

    ground_truth_file.close()

    vul_filenames = list(ground_truth.keys())

    for filename in vul_filenames:
        SRC_PATH = os.path.join(FIXED_HEADER_FOLDER, filename)
        DST_PATH = os.path.join(SOURCE_CODE_PATH, filename)
        shutil.copyfile(SRC_PATH, DST_PATH)

if __name__ == "__main__":
    main()