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
    SRC_PATH = os.path.join(PROJ_PATH, config.src_folder)
    IGNORED_FILES_FOLDER = os.path.join(PROJ_PATH, config.ignored_files_folder)
    IGNORE_LIST_PATH = os.path.join(PROJ_PATH, config.ignore_list_path)

    ignore_list = dict()
    with open(IGNORE_LIST_PATH, "r") as f:
        ignore_list = json.load(f)

    for filename in ignore_list["ignore_list"]:
        shutil.copyfile(f"{os.path.join(SRC_PATH, filename)}", f"{os.path.join(IGNORED_FILES_FOLDER, filename)}")

if __name__ == "__main__":
    main()