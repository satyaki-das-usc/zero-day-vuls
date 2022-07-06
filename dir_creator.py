import os
import json
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

    if not os.path.isdir(CVE_PATH):
        os.mkdir(CVE_PATH)
    if not os.path.isdir(PROJ_PATH):
        os.mkdir(PROJ_PATH)

    for foldername in data_format["folders"].keys():
        FOLDER_PATH = os.path.join(PROJ_PATH, data_format["folders"][foldername])
        if not os.path.isdir(FOLDER_PATH):
            os.mkdir(FOLDER_PATH)
    
    empty_dict = dict()

    for filename in data_format["files"].keys():
        FILE_PATH = os.path.join(PROJ_PATH, data_format["files"][filename])
        if not os.path.isfile(FILE_PATH):
            os.system(f"touch {FILE_PATH}")
            with open(FILE_PATH, 'w') as f:
                json.dump(empty_dict, f, indent=2)
    
    IGNORE_LIST_PATH = os.path.join(PROJ_PATH, data_format["ignore_list_path"])

    if not os.path.isfile(IGNORE_LIST_PATH):
        os.system(f"touch {IGNORE_LIST_PATH}")
        empty_dict["ignore_list"] = []
        with open(IGNORE_LIST_PATH, 'w') as ignore_list_file:
            json.dump(empty_dict, ignore_list_file, indent=2)

if __name__ == "__main__":
    main()