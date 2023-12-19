# Image Sequencer Compressor

## Description
The `ImageSequencerCompressor.py` is a Python script designed for efficient management of large image collections. It searches through nested directories for sequential image files and compresses them into ZIP files, while also cleaning up the directory by retaining only the first image in each sequence.

## Features
- Automated scanning of directories for sequential images.
- Compression of image sequences into ZIP files.
- Deletion of all but the first image in each sequence to reduce clutter.
- Support for various naming patterns of image files.

## Important Notice
**Warning**: This script will *delete* all images in a sequence after compressing them into a ZIP file, **except** for the first image in each sequence. Please ensure you have backups or are comfortable with this operation before running the script. This action cannot be undone and is intended to save space and reduce file clutter in large image collections.

## How to Use
1. Place the `ImageSequencerCompressor.py` in the root directory where you want to start the search.
2. Run the script using Python 3.
3. The script will scan all subdirectories and identify image sequences.
4. Once a sequence is found, it will compress the images and keep only the first one.
5. The script will display the paths of the compressed files and retained images.

Executable File:
- The `ImageSequencerCompressor.exe` is the executable version of the script, which can be run on Windows without the need for a Python installation.
- Simply download and place it in the root directory where you wish to process images.
- Run the executable to start the compression process.
 
## Requirements
- Python 3.x
- Basic knowledge of command line operations

## License
This script is released under the MIT License. See the LICENSE file for more details.
