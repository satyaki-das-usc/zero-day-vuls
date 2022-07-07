#!/bin/bash

PYTHONPATH="." python dir_creator.py
PYTHONPATH="." python extract_src_files.py
PYTHONPATH="." python header_files_fixer.py
PYTHONPATH="." python ignored_file_copier.py
echo "Phase 1 is complete. Remember to do the following:"
echo "1. Fix the ignored files.\n"
echo "2. Ensure ground truth file is updated."
echo "3. Update the config file in the model directory"