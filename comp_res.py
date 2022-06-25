import json
import os

RES1_FILE = "vul_files-1.0.2-beta1.json"
RES2_FILE = "vul_files-1.0.2-beta2.json"

vul_filenames = ["d1_both.c", "t1_lib.c"]

def main():
    results1_file = open(RES1_FILE)
    results1 = json.load(results1_file)

    results1_file.close()

    results2_file = open(RES2_FILE)
    results2 = json.load(results2_file)

    results2_file.close()

    for filename in vul_filenames:
        for i in range(min(len(results1[filename]), len(results2[filename]))):
            if results1[filename][i] != results2[filename][i]:
                print(filename, i)

    # for vf in vul_filenames:
    #     if results1[vf] != results2[vf]:
    #         print(results1[vf], results2[vf])
    


if __name__ == "__main__":
    main()