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
    GROUND_TRUTH_PATH = os.path.join(PROJ_PATH, config.ground_truth_path)
    RESULTS_PATH = os.path.join(PROJ_PATH, config.results_path)
    SELECT_RESULTS_PATH = os.path.join(PROJ_PATH, config.select_results_path)
    VUL_SLICES_PATH = os.path.join(PROJ_PATH, config.vul_slices_path)

    MODEL_CVE_DATA_FOLDER = os.path.join(config.model_data_folder, config.dataset.cve_id)
    RESULTS_JSON_FILE_PATH = os.path.join(MODEL_CVE_DATA_FOLDER, "results.json")

    model_folder_path = config.model_data_folder.replace("data", "")[:-1]
    MODEL_SELECT_RESULTS_PATH = os.path.join(model_folder_path, "select_results.json")
    
    shutil.copyfile(RESULTS_JSON_FILE_PATH, RESULTS_PATH)
    shutil.copyfile(MODEL_SELECT_RESULTS_PATH, SELECT_RESULTS_PATH)
    
    results_file = open(SELECT_RESULTS_PATH)
    results = json.load(results_file)

    results_file.close()

    ground_truth_file = open(GROUND_TRUTH_PATH)
    ground_truth = json.load(ground_truth_file)

    ground_truth_file.close()

    vul_filenames = list(ground_truth.keys())

    vul_results = {}

    for filename in vul_filenames:
        vul_results[filename] = []
        for entry in results[filename]:
            if entry[1] == 1:
                if vul_results[filename].count(entry) < 1:
                        vul_results[filename].append(entry)

    with open(VUL_SLICES_PATH, 'w') as select_results_file:
        json.dump(vul_results, select_results_file, indent=2)
        


if __name__ == "__main__":
    main()