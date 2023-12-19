# Copyright (c) 2023 IleriKod Solutions
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# English:
# ImageSequencerCompressor.py: A Python script to compress sequential images in folders.
# It searches for image sequences and compresses them into ZIP files, keeping only the first image.

# Türkçe:
# ImageSequencerCompressor.py: Klasörlerdeki ardışık resimleri sıkıştırmak için bir Python betiği.
# Resim dizilerini arar ve sadece ilk resmi tutarak bunları ZIP dosyalarına sıkıştırır.

# العربية:
# ImageSequencerCompressor.py: سكربت بايثون لضغط الصور المتسلسلة في المجلدات.
# يبحث عن تسلسلات الصور ويضغطها في ملفات ZIP، مع الاحتفاظ بالصورة الأولى فقط.

import os
import re
import zipfile

def find_folders_for_compression(base_path):
    # This function searches for image sequences in the given directory and its subdirectories.
    folders_to_compress = {}
    for root, dirs, files in os.walk(base_path):
        files_dict = {}
        for file in files:
            # Match files based on the naming pattern.
            match = re.match(r'(.*?)(\(\d+\))?(\d+)\.png', file)
            if match:
                key = match.group(1)
                files_dict.setdefault(key, []).append(file)

        # Add folders with more than 10 matching files to the list for compression.
        for key, file_list in files_dict.items():
            if len(file_list) >= 10:
                folders_to_compress[root] = (key, file_list)

    return folders_to_compress

def ask_to_compress(folders_to_compress):
    # Ask the user whether to compress the identified folders.
    if not folders_to_compress:
        print("No sequential images were found to compress.")
        return

    for folder, (key, file_list) in folders_to_compress.items():
        print(f"Folder: {folder}, Name: {key}, Number of Images: {len(file_list)}")
    response = input("Do you want to compress these folders? (yes/no): ")
    if response.lower() == 'yes':
        compress_folders(folders_to_compress)

def compress_folders(folders_to_compress):
    # Compress the images in each folder and delete all but the first image.
    for folder, (key, file_list) in folders_to_compress.items():
        zip_filename = os.path.join(folder, f'{key}.zip')
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for file in file_list:
                zipf.write(os.path.join(folder, file), file)

        # Delete all but the first image.
        for file in file_list[1:]:
            os.remove(os.path.join(folder, file))

        print(f'Compressed {len(file_list)} images into {zip_filename} and kept the first one.')

# Main execution
if __name__ == "__main__":
    # Set the current directory as the base path for searching images.
    base_path = os.getcwd()
    folders_to_compress = find_folders_for_compression(base_path)
    ask_to_compress(folders_to_compress)

