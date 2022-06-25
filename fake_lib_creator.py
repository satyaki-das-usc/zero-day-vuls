import os
import shutil

REAL_LIB_PATH = "data/CVE-2014-0160/openssl-1.0.2-beta1/git-repo/include/openssl"
FAKE_LIB_PATH = "fake_ssl_lib"

def main():
    if not os.path.isdir(FAKE_LIB_PATH):
        os.mkdir(FAKE_LIB_PATH)

    real_libs = os.listdir(REAL_LIB_PATH)

    for filename in real_libs:
        content = ""
        with open(os.path.join(REAL_LIB_PATH, filename), "r") as f:
            content = f.read()
        
        output_filename = os.path.join(FAKE_LIB_PATH, filename)
        os.system(f"touch {output_filename}")

        with open(output_filename, "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()