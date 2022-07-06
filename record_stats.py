import os
from os.path import join, isdir, isfile
import json
from pandas import DataFrame
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))

    DATA_FORMAT_FILENAME = os.path.join(config.data_folder, config.data_format_filename)

    with open(DATA_FORMAT_FILENAME, "r") as f:
        data_format = json.load(f)

    CVE_IDs = []
    test_subjects = []
    contents = []
    
    for filename in os.listdir(config.data_folder):
        cve_folder = join(config.data_folder, filename)
        if isdir(cve_folder) and filename.startswith("CVE"):
            cve_id = filename
            for test_subject_name in os.listdir(cve_folder):
                test_subject_folder = join(cve_folder, test_subject_name)
                STATS_PATH = join(test_subject_folder, data_format["files"]["stats_path"])
                CVE_IDs.append(cve_id)
                test_subjects.append(test_subject_name)

                if isfile(STATS_PATH):
                    with open(STATS_PATH, "r") as f:
                        contents.append(f.read())
                else:
                    contents.append("FILE DOES NOT EXIST.")
    
    df = DataFrame(
        {
            "CVE ID": CVE_IDs,
            "Test Subject": test_subjects,
            "Content in \"stats.txt\"": contents
        }
    )
    
    EXCEL_PATH = "test_results.xlsx"

    if not isfile(EXCEL_PATH):
        os.system(f"touch {EXCEL_PATH}")
    
    df.to_excel(EXCEL_PATH, sheet_name='Test Result', index=False)


if __name__ == "__main__":
    main()