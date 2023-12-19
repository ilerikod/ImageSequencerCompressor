Description:
The ImageSequencerCompressor.py is a Python script designed for efficient management of large image collections. It searches through nested directories for sequential image files and compresses them into ZIP files, while also cleaning up the directory by retaining only the first image in each sequence.

Features:

Automated scanning of directories for sequential images.
Compression of image sequences into ZIP files.
Deletion of all but the first image in each sequence to reduce clutter.
Support for various naming patterns of image files.
How to Use:

Place the ImageSequencerCompressor.py in the root directory where you want to start the search.
Run the script using Python 3.
The script will scan all subdirectories and identify image sequences.
Once a sequence is found, it will compress the images and keep only the first one.
The script will display the paths of the compressed files and retained images.
Requirements:

Python 3.x
Basic knowledge of command line operations
License:
This script is released under the MIT License. See the LICENSE file for more details.
