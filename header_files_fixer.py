import os
import json
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))
    
    CVE_PATH = os.path.join(config.data_folder, config.dataset.cve_id)
    PROJ_PATH = os.path.join(CVE_PATH, config.dataset.project_name)
    SRC_PATH = os.path.join(PROJ_PATH, config.src_folder)
    FIXED_HEADER_FOLDER = os.path.join(PROJ_PATH, config.fixed_header_folder)
    IGNORE_LIST_PATH = os.path.join(PROJ_PATH, config.ignore_list_path)

    ignore_list = dict()
    with open(IGNORE_LIST_PATH, "r") as f:
        ignore_list = json.load(f)

    for filename in os.listdir(SRC_PATH):

        if filename in ignore_list["ignore_list"]:
            continue
        content = ""

        with open(os.path.join(SRC_PATH, filename), "r") as f:
            print(filename)
            try:
                content = f.readlines()

                fixed_content = []
                for line in content:
                    fixed_line = line
                    if "include \"" in line:
                        fixed_str = "#include \""
                        fixed_line = fixed_line.replace(fixed_str, "")
                        tokens = fixed_line.split("/")
                        fixed_line = f"{fixed_str}{tokens[-1]}"
                    
                    fixed_content.append(fixed_line)
            except Exception as e:
                print(f"Error <{e}> occurred. Adding to ignore list.")
                ignore_list["ignore_list"].append(filename)
                continue
        
        dst_file_path = os.path.join(FIXED_HEADER_FOLDER, filename)
        if not os.path.isfile(dst_file_path):
            os.system(f"touch {dst_file_path}")
        with open(dst_file_path, "w") as f:
            f.writelines(fixed_content)
    
    with open(IGNORE_LIST_PATH, "w") as f:
        json.dump(ignore_list, f, indent=2)

if __name__ == "__main__":
    main()