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
    IGNORED_FILES_FOLDER = os.path.join(PROJ_PATH, data_format["folders"]["ignored_files_folder"])
    IGNORE_LIST_PATH = os.path.join(PROJ_PATH, data_format["ignore_list_path"])
    
    ignore_list = dict()
    with open(IGNORE_LIST_PATH, "r") as f:
        ignore_list = json.load(f)

    for filename in ignore_list["ignore_list"]:
        shutil.copyfile(f"{os.path.join(IGNORED_FILES_FOLDER, filename)}", f"{os.path.join(FIXED_HEADER_FOLDER, filename)}")

if __name__ == "__main__":
    main()