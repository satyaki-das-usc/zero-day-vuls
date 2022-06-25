import os
import json
from turtle import st

SLICE_FILE_PATH = "slice_data.json"
LINES_FILE_PATH = "vulnerable_lines.json"
FOCUS_FILE_PATH = "focus.json"

def main():
    slice_file = open(SLICE_FILE_PATH)
    slice_data = json.load(slice_file)
    slice_file.close()

    lines_file = open(LINES_FILE_PATH)
    lines_data = json.load(lines_file)
    lines_file.close()

    focus_data = {}

    for key, value in lines_data.items():
        data = {}
        for line in value:
            slice_set = []
            for slice in slice_data[key]:
                if str(line) in slice:
                    slice_set.append(slice)
            
            data[str(line)] = slice_set
        
        focus_data[key] = data
    
    with open(FOCUS_FILE_PATH, "w") as outfile:
        json.dump(focus_data, outfile)
            

if __name__ == "__main__":
    main()