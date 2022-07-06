#!/bin/bash

PYTHONPATH="." python ignored_file_placer.py
PYTHONPATH="." python run_model.py
PYTHONPATH="." python select_result_analysis.py
PYTHONPATH="." python record_stats.py
# PYTHONPATH="." python vul_slice_extractor.py
# PYTHONPATH="." python vul_checker.py