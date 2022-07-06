import os
import json
import shutil
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    # os.mkdir(DST_PATH)
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))
    
    PROJ_PATH = os.path.join(os.path.join(config.data_folder, config.dataset.cve_id), config.dataset.project_name)
    DATA_FORMAT_FILENAME = os.path.join(config.data_folder, config.data_format_filename)

    with open(DATA_FORMAT_FILENAME, "r") as f:
        data_format = json.load(f)
    
    SRC_PATH = os.path.join(PROJ_PATH, data_format["folders"]["repo_folder"])
    DST_PATH = os.path.join(PROJ_PATH, data_format["folders"]["src_folder"])
    src_file_paths = []
    dst_file_paths = []

    __len = 0

    c_cpp_src_file_extensions = [".h", ".c", ".cpp", ".cc"]

    for root, __, files in os.walk(SRC_PATH):
        for src_filename in files:
            for file_extension in c_cpp_src_file_extensions:
                if src_filename.endswith(file_extension):
                    if len(__) > 0:
                        __len += 1
                    src_file_paths.append(os.path.join(root, src_filename))
                    
                    dst_filename = os.path.join(DST_PATH, src_filename)
                    offset = -1 * len(file_extension)
                    while dst_filename in set(dst_file_paths):
                            dst_filename = f"{dst_filename[:offset]}0{file_extension}"
                    dst_file_paths.append(dst_filename)
    
    # print(len(src_file_paths), __len, (len(src_file_paths) - __len))
    
    for i in range(len(src_file_paths)):
        shutil.copyfile(src_file_paths[i], dst_file_paths[i])


if __name__ == "__main__":
    main()