import os
import shutil

SRC_PATH = 'data/2015-10-27-openssl-v1-0-1e/source-code'
DST_PATH = 'data/2015-10-27-openssl-v1-0-1e/just-src-files'

def main():
    # os.mkdir(DST_PATH)
    src_file_paths = []
    dst_file_paths = []
    for root, unk, files in os.walk(SRC_PATH):
        for src_filename in files:
            if src_filename.endswith(".c"):
                src_file_paths.append(f"{root}/{src_filename}")
                
                dst_root = root.replace(f"{SRC_PATH}/", "")
                pos = dst_root.find("/")
                dst_root = dst_root[:pos] + "/testcases" + dst_root[pos:]
                dst_root = DST_PATH + "/" + dst_root
                dst_filename = f"{src_filename}"
                while dst_filename in set(dst_file_paths):
                    dst_filename = f"{dst_filename[:-2]}0.c"
                dst_file_paths.append(dst_filename)

    # # print(len(src_file_paths))

    # # for dst_path in dst_file_paths:
    # #     dirs_inside = dst_path[0].split("/")
    # #     dest_dir = DST_PATH
    # #     for curr_dir in dirs_inside:
    # #         dest_dir += "/" + curr_dir
    # #         if not os.path.isdir(dest_dir):
    # #             os.mkdir(dest_dir)
    
    for i in range(len(src_file_paths)):
        shutil.copyfile(src_file_paths[i], f"{DST_PATH}/{dst_file_paths[i]}")
    
    # libs = list(filter(lambda x: "eng_lib" in x, all_files))

    # eng_lib_0_file = open(libs[0], "r")
    # eng_lib_1_file = open(libs[1], "r")

    # eng_lib_0_txt = eng_lib_0_file.read()
    # eng_lib_1_txt = eng_lib_1_file.read()

    # eng_lib_0_file.close()
    # eng_lib_1_file.close()

    # assert eng_lib_0_txt == eng_lib_1_txt


if __name__ == "__main__":
    main()