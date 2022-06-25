import os
import json

SRC_FILE_PATH = "slice_info.txt"
DST_FILE_PATH = "slice_data.json"

def main():
    txt_file = open(SRC_FILE_PATH, "r")
    lines = list(map(lambda x: x.strip(), txt_file.readlines()))
    txt_file.close()

    slice_lines = {}

    for ln in lines:
        (key, value) = ln.split("->")
        value = value.replace("[", "")
        value = value.replace("]", "")
        value = list(map(lambda x: x.strip(), value.split(",")))
        # print(value)
        # value = list(filter(lambda x: len(x) == 1 and x[0] == "", value))
        if "" not in value:
            if key in slice_lines.keys():
                slice_lines[key].append(value)
            else:
                slice_lines[key] = []
                slice_lines[key].append(value)

    for key, value in slice_lines.items():
        print(key, len(value))

    with open(DST_FILE_PATH, "w") as outfile:
        json.dump(slice_lines, outfile)

if __name__ == "__main__":
    main()