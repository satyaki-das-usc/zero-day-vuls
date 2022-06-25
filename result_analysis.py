import json
import os

def main():
    results_file = open("data/openssl-heartbleed/results-1.0.2-beta2.json")
    results = json.load(results_file)

    vul_files = {}

    total_files_count = len(results.keys())

    total_slice_count = 0
    vul_slice_count = 0

    for c_file in results.keys():
        curr_results = results[c_file]
        total_slice_count += len(curr_results)
        vul_slices_per_file = sum(curr_results)
        if vul_slices_per_file > 0:
            vul_files[c_file] = curr_results
            vul_slice_count += vul_slices_per_file


    results_file.close()

    vul_files_count = len(vul_files.keys())

    print(f"{vul_files_count} out of {total_files_count} files contain vulnerable slices")
    print(f"{vul_slice_count} out of {total_slice_count} slices are vulnerable")

    # vul_files_json = json.dumps(vul_files, indent=4)

    outfilename = "vul_files-1.0.2-beta2.json"

    os.system(f"touch {outfilename}")

    with open(outfilename, "w") as outfile:
        json.dump(vul_files, outfile)
    


if __name__ == "__main__":
    main()