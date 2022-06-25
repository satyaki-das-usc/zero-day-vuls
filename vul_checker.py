import os
import json
from typing import cast
from omegaconf import OmegaConf, DictConfig

CONF_PATH = "configs/dwk.yaml"

def main():
    config = cast(DictConfig, OmegaConf.load(CONF_PATH))

    CVE_PATH = os.path.join(config.data_folder, config.dataset.cve_id)
    PROJ_PATH = os.path.join(CVE_PATH, config.dataset.project_name)
    GROUND_TRUTH_PATH = os.path.join(PROJ_PATH, config.ground_truth_path)
    SELECT_RESULTS_PATH = os.path.join(PROJ_PATH, config.select_results_path)

    results_file = open(SELECT_RESULTS_PATH)
    results = json.load(results_file)

    results_file.close()

    ground_truth_file = open(GROUND_TRUTH_PATH)
    ground_truth = json.load(ground_truth_file)

    ground_truth_file.close()

    vul_filenames = list(ground_truth.keys())

    focus_slices = {}

    for filename in vul_filenames:
        focus_slices[filename] = []
        for vul_line in ground_truth[filename]:
            for entry in results[filename]:
                if vul_line in entry[0]:
                    if focus_slices[filename].count(entry) < 1:
                        focus_slices[filename].append(entry)
    
    FOCUS_SLICES_PATH = os.path.join(PROJ_PATH, "focus.json")

    if not os.path.isfile(FOCUS_SLICES_PATH):
        os.system(f"touch {FOCUS_SLICES_PATH}")

    with open(FOCUS_SLICES_PATH, 'w') as focus_slice_file:
        json.dump(focus_slices, focus_slice_file, indent=2)
    
    focus_slice_count = 0
    desired_output = config.desired_output

    generated_desired_output_count = 0
    for filename in vul_filenames:
        slice_result_list = focus_slices[filename]
        focus_slice_count += len(slice_result_list)

        for entry in slice_result_list:
            if entry[1] == desired_output:
                generated_desired_output_count += 1
    
    OUTPUT_TEXT_FILE_PATH = os.path.join(PROJ_PATH, "stats.txt")

    if not os.path.isfile(OUTPUT_TEXT_FILE_PATH):
        os.system(f"touch {OUTPUT_TEXT_FILE_PATH}")
    
    with open(OUTPUT_TEXT_FILE_PATH, "w") as outputfile:
        if focus_slice_count == 0:
            outputfile.write(f"Desired slices were not generated. Testcase level prediction:\n")
            for filename in vul_filenames:
                preds = list(map(lambda x: x[1], results[filename]))
                testcase_level_pred = 1 in preds
                categories = ["Non-vulnerable", "Vulnerable"]
                outputfile.write(f"{filename}: {categories[int(testcase_level_pred)]}\n")
        else:
            outputfile.write(f"Correctly guessed: {generated_desired_output_count} out of {focus_slice_count} slice(s).\nAccuracy: {(generated_desired_output_count / focus_slice_count) * 100}%")
    

if __name__ == "__main__":
    main()