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
    
    FIXED_HEADER_FOLDER = os.path.join(PROJ_PATH, data_format["folders"]["fixed_header_folder"])
    GROUND_TRUTH_PATH = os.path.join(PROJ_PATH, data_format["files"]["ground_truth_path"])
    RESULTS_PATH = os.path.join(PROJ_PATH, data_format["files"]["results_path"])
    SELECT_RESULTS_PATH = os.path.join(PROJ_PATH, data_format["files"]["select_results_path"])
    
    MODEL_DATA_FOLDER = config.model_data_folder
    MODEL_CVE_DATA_FOLDER = os.path.join(MODEL_DATA_FOLDER, config.dataset.cve_id)
    DST_W2V_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "w2v.wv")
    ALL_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "all.json")
    RESULTS_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "results.json")
    DONE_TXT_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "done.txt")
    MODEL_GROUND_TRUTH_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, data_format["files"]["ground_truth_path"])
    CSV_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "csv")
    XFG_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "XFG")
    SOURCE_CODE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "source-code")

    folders = [MODEL_CVE_DATA_FOLDER, SOURCE_CODE_PATH]

    for foldername in folders:
        if not os.path.isdir(foldername):
            os.mkdir(foldername)
    
    if not os.path.isfile(DST_W2V_PATH):
        SRC_W2V_PATH  = os.path.join(MODEL_CVE_DATA_FOLDER.replace(config.dataset.cve_id, "CWE119"), "w2v.wv")
        shutil.copyfile(SRC_W2V_PATH, DST_W2V_PATH)


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

    for filename in os.listdir(FIXED_HEADER_FOLDER):
        SRC_PATH = os.path.join(FIXED_HEADER_FOLDER, filename)
        DST_PATH = os.path.join(SOURCE_CODE_PATH, filename)
        shutil.copyfile(SRC_PATH, DST_PATH)
    
    shutil.copyfile(GROUND_TRUTH_PATH, MODEL_GROUND_TRUTH_PATH)
    
    model_folder_path = MODEL_DATA_FOLDER.replace("data", "")[:-1]

    cwd = os.getcwd()
    os.chdir(model_folder_path)

    os.system(f"PYTHONPATH=\".\" python src/joern/joern-parse.py")
    os.system(f"PYTHONPATH=\".\" python src/data_generator.py")
    os.system(f"PYTHONPATH=\".\" python src/preprocess/dataset_generator.py")
    os.system(f"PYTHONPATH=\".\" python src/evaluate.py --dataset-name {config.dataset.cve_id} DeepWukong")
    
    os.chdir(cwd)
    # print(f"pushd {model_folder_path}")
    # print(evaluate_str)

    MODEL_SELECT_RESULTS_PATH = os.path.join(model_folder_path, data_format["files"]["select_results_path"])

    shutil.copyfile(RESULTS_JSON_FILE_PATH, RESULTS_PATH)
    shutil.copyfile(MODEL_SELECT_RESULTS_PATH, SELECT_RESULTS_PATH)

if __name__ == "__main__":
    main()