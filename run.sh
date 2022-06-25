PYTHONPATH="." python dir_creator.py
PYTHONPATH="." python extract_src_files.py
PYTHONPATH="." python header_files_fixer.py
PYTHONPATH="." python ignored_file_copier.py
PYTHONPATH="." python ignored_file_placer.py
PYTHONPATH="." python run_model.py
PYTHONPATH="." python vul_slice_extractor.py
PYTHONPATH="." python vul_checker.py

rm /home/satyaki/luka/DeepWukongCopy/data/CVE-2013–1892/source-code/*
rm data/CVE-2013–1892/mongo-r2.2.3/git-repo/*
cp mongo-r2.2.3/* /home/satyaki/luka/zero-day-vuls/data/CVE-2013–1892/mongo-r2.2.3/git-repo

cp data/CVE-2013–1892/mongo-r2.2.3/fixed-src-files/* /home/satyaki/luka/DeepWukongCopy/data/CVE-2013–1892/source-code
rm /home/satyaki/luka/DeepWukongCopy/data/CVE-2014-0160/source-code/*
rm -rf /home/satyaki/luka/DeepWukongCopy/data/CVE-2014-0160/csv
rm -rf /home/satyaki/luka/DeepWukongCopy/data/CVE-2014-0160/XFG
cp data/CVE-2014-0160/openssl-1.0.1f/fixed-src-files/* /home/satyaki/luka/DeepWukongCopy/data/CVE-2014-0160/source-code
