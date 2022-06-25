import os
import shutil
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    # os.mkdir(DST_PATH)
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))
    
    PROJ_PATH = os.path.join(os.path.join(config.data_folder, config.dataset.cve_id), config.dataset.project_name)
    SRC_PATH = os.path.join(PROJ_PATH, config.repo_folder)
    DST_PATH = os.path.join(PROJ_PATH, config.src_folder)
    src_file_paths = []
    dst_file_paths = []

    __len = 0

    for root, __, files in os.walk(SRC_PATH):
        for src_filename in files:
            if src_filename.endswith(".c") or src_filename.endswith(".cpp") or src_filename.endswith(".h"):
                if len(__) > 0:
                    __len += 1
                src_file_paths.append(os.path.join(root, src_filename))
                
                dst_filename = os.path.join(DST_PATH, src_filename)
                if src_filename.endswith(".c"):
                    while dst_filename in set(dst_file_paths):
                        dst_filename = f"{dst_filename[:-2]}0.c"
                elif src_filename.endswith(".cpp"):
                    while dst_filename in set(dst_file_paths):
                        dst_filename = f"{dst_filename[:-4]}0.cpp"
                dst_file_paths.append(dst_filename)
    
    # print(len(src_file_paths), __len, (len(src_file_paths) - __len))
    
    for i in range(len(src_file_paths)):
        shutil.copyfile(src_file_paths[i], dst_file_paths[i])


if __name__ == "__main__":
    main()