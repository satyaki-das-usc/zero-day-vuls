import os
import json
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))
    
    CVE_PATH = os.path.join(config.data_folder, config.dataset.cve_id)
    PROJ_PATH = os.path.join(CVE_PATH, config.dataset.project_name)
    REPO_PATH = os.path.join(PROJ_PATH, config.repo_folder)
    SRC_PATH = os.path.join(PROJ_PATH, config.src_folder)
    FIXED_HEADER_FOLDER = os.path.join(PROJ_PATH, config.fixed_header_folder)
    IGNORED_FILES_FOLDER = os.path.join(PROJ_PATH, config.ignored_files_folder)
    SELECT_RESULTS_PATH = os.path.join(PROJ_PATH, config.select_results_path)
    RESULTS_PATH = os.path.join(PROJ_PATH, config.results_path)
    GROUND_TRUTH_PATH = os.path.join(PROJ_PATH, config.ground_truth_path)
    VUL_SLICES_PATH = os.path.join(PROJ_PATH, config.vul_slices_path)
    IGNORE_LIST_PATH = os.path.join(PROJ_PATH, config.ignore_list_path)

    if not os.path.isdir(CVE_PATH):
        os.mkdir(CVE_PATH)
    if not os.path.isdir(PROJ_PATH):
        os.mkdir(PROJ_PATH)
    if not os.path.isdir(REPO_PATH):
        os.mkdir(REPO_PATH)
    if not os.path.isdir(SRC_PATH):
        os.mkdir(SRC_PATH)
    if not os.path.isdir(FIXED_HEADER_FOLDER):
        os.mkdir(FIXED_HEADER_FOLDER)
    if not os.path.isdir(IGNORED_FILES_FOLDER):
        os.mkdir(IGNORED_FILES_FOLDER)
    
    empty_dict = dict()
    
    if not os.path.isfile(SELECT_RESULTS_PATH):
        os.system(f"touch {SELECT_RESULTS_PATH}")
        with open(SELECT_RESULTS_PATH, 'w') as f:
            json.dump(empty_dict, f, indent=2)
    if not os.path.isfile(RESULTS_PATH):
        os.system(f"touch {RESULTS_PATH}")
        with open(RESULTS_PATH, 'w') as f:
            json.dump(empty_dict, f, indent=2)
    if not os.path.isfile(GROUND_TRUTH_PATH):
        os.system(f"touch {GROUND_TRUTH_PATH}")
        with open(GROUND_TRUTH_PATH, 'w') as f:
            json.dump(empty_dict, f, indent=2)
    if not os.path.isfile(VUL_SLICES_PATH):
        os.system(f"touch {VUL_SLICES_PATH}")
        with open(VUL_SLICES_PATH, 'w') as f:
            json.dump(empty_dict, f, indent=2)
    if not os.path.isfile(IGNORE_LIST_PATH):
        os.system(f"touch {IGNORE_LIST_PATH}")
        empty_dict["ignore_list"] = []
        with open(IGNORE_LIST_PATH, 'w') as ignore_list_file:
            json.dump(empty_dict, ignore_list_file, indent=2)

if __name__ == "__main__":
    main()