import os
import json

SLICE_FILE_PATH = "slice_data.json"
RESULTS_FILE_PATH = "data/openssl-heartbleed/results-1.0.2-beta1.json"
DST_FILE_PATH = "vul_slices.json"

def main():
    slice_file = open(SLICE_FILE_PATH)
    slice_data = json.load(slice_file)
    slice_file.close()

    results_file = open(RESULTS_FILE_PATH)
    results_data = json.load(results_file)
    results_file.close()

    vul_filenames = ["d1_both.c", "t1_lib.c"]

    vul_slices = {}

    for filename in vul_filenames:
        print(len(slice_data[filename]), len(results_data[filename]))
        # assert len(slice_data[filename]) == len(results_data[filename])
        vul_slices[filename] = []
        for i in range(len(results_data[filename])):
            if results_data[filename][i] == 1:
                vul_slices[filename].append(slice_data[filename][i])
    
    with open(DST_FILE_PATH, "w") as outfile:
        json.dump(vul_slices, outfile)

if __name__ == "__main__":
    main()