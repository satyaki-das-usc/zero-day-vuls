#!/bin/bash

PYTHONPATH="." python dir_creator.py
PYTHONPATH="." python extract_src_files.py
PYTHONPATH="." python header_files_fixer.py
PYTHONPATH="." python ignored_file_copier.py