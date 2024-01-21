from glob import glob
import os

files = glob('**/*.py', recursive=True)

merged_files = ""

for file in files:
    with open(file, 'r') as f:
        content = f.read() + "\n\n"
    
    merged_files += "# Path: " + os.path.basename(file) + "\n"
    merged_files += content

with open('merged_files.txt', 'w') as f:
    f.write(merged_files)