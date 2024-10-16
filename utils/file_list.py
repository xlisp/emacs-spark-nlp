import re
import os

def find_files_with_chinese_names(directory):
    chinese_file_paths = []

    # Regular expression to match Chinese characters
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]+')

    # Walk through the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            # Check if the file name contains any Chinese characters
            if chinese_pattern.search(file):
                # Add the full path to the result list
                #chinese_file_paths.append(("", os.path.join(root, file)))
                chinese_file_paths.append(("", file))

    return chinese_file_paths

