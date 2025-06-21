import os
import re

def rename_bin_files(folder_path: str):
    # Match pattern: bin1.#
    pattern = re.compile(r'^bin1\.(\d+)$')
    
    files = os.listdir(folder_path)
    
    # Extract matching files with numeric index
    matched_files = [(int(m.group(1)), f) for f in files if (m := pattern.match(f))]

    # Sort by numeric index
    matched_files.sort()

    for idx, (_, old_name) in enumerate(matched_files, start=1):
        new_name = f"bin{idx}.fa"
        old_path = os.path.join(folder_path, old_name)
        new_path = os.path.join(folder_path, new_name)
        os.rename(old_path, new_path)
        print(f"Renamed {old_name} -> {new_name}")

if __name__ == "__main__":
    rename_bin_files("MetaBAT_bin1")