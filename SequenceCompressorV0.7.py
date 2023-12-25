import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext
import os
import re
import zipfile
import threading

# Global variables
thread_done = False
total_images_found = 0

# Function to display messages in the text box
def log_message(message, color, path=None):
    log_text.config(state='normal')
    tag_name = f"color_{int(log_text.index('end-1c').split('.')[0])}"
    log_text.tag_config(tag_name, foreground=color)

    if path:
        # Replace forward slashes with backslashes for path display
        display_path = path.replace('/', '\\')
        log_text.insert(tk.END, f"Path: {display_path}\n", tag_name)

    log_text.insert(tk.END, f"{message}\n", tag_name)
    log_text.config(state='disabled')
    log_text.yview(tk.END)

# Function to run image compression in a separate thread
def compress_images_thread(extension, folder_path):
    thread = threading.Thread(target=compress_images, args=(extension, folder_path))
    thread.start()

# Function to compress images
def compress_images(extension, folder_path):
    global thread_done
    global total_images_found
    
    for root, dirs, files in os.walk(folder_path):
        files_dict = {}
        for file in files:
            if file.endswith(extension):
                log_message(f"Found {file} in {root}", "grey")  # Log message
                match = re.match(r'(.*?)(\d+)\.{}'.format(extension.strip('.')), file)
                if not match:
                    # Try to match any character string before the extension
                    match = re.match(r'(.*?)\.{}'.format(extension.strip('.')), file)
                if match:
                    key = match.group(1)
                    files_dict.setdefault(key, []).append(file)

        for key, file_list in files_dict.items():
            if len(file_list) >= 10:
                progress_var.set(0)  # Reset progress bar
                app.update_idletasks()  # Update the UI
                zip_filename = os.path.join(root, f'{key}.zip').replace('/', '\\')
                with zipfile.ZipFile(zip_filename, 'w') as zipf:
                    for i, file in enumerate(file_list):
                        zipf.write(os.path.join(root, file), file)
                        progress_var.set((i + 1) / len(file_list) * 100)  # Update progress bar
                        app.update_idletasks()  # Update the UI
                
                # Delete all images except the first one after compression
                for file in file_list[1:]:
                    os.remove(os.path.join(root, file))
                log_message(f"Compressed {len(file_list)} images in {zip_filename}", "blue")
                total_images_found += len(file_list)
    thread_done = True
    
# Function to run image decompression in a separate thread
def decompress_images_thread(folder_path):
    thread = threading.Thread(target=decompress_images, args=(folder_path,))
    thread.start()

# Function to decompress images
def decompress_images(folder_path):
    global thread_done
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file).replace('/', '\\')
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    extracted_files = zip_ref.namelist()

                    progress_var.set(0)  # Reset progress bar
                    app.update_idletasks()  # Update the UI

                    for i, file in enumerate(extracted_files):
                        zip_ref.extract(file, root)
                        progress_var.set((i + 1) / len(extracted_files) * 100)  # Update progress bar
                        app.update_idletasks()  # Update the UI

                log_message(f"Decompressed images in {zip_path}", "green")
    thread_done = True

# Function to select a folder for compression
def select_folder_for_compression():
    folder_path = filedialog.askdirectory()
    if folder_path:
        compress_images(extension_var.get(), folder_path)

# Function to select a folder for decompression
def select_folder_for_decompression():
    folder_path = filedialog.askdirectory()
    if folder_path:
        decompress_images(folder_path)

# Function to select a folder
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_path_var.set(folder_path)

# Function to start compression
def start_compression():
    if messagebox.askyesno("Start Compression", "Do you want to start compression?"):
        global thread_done
        thread_done = False
        compress_images_thread(extension_var.get(), folder_path_var.get())
        check_thread()

# Function to start decompression
def start_decompression():
    folder_path = folder_path_var.get()
    if folder_path:
        global thread_done
        thread_done = False
        decompress_images_thread(folder_path)
        check_thread()

# Function to save the log to a file
def save_log_to_file():
    content = log_text.get("1.0", tk.END)
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(content)
        messagebox.showinfo("Save Report", f"Report saved to {file_path}")

# Function to check the thread status
def check_thread():
    if thread_done:
        messagebox.showinfo("Operation Completed", f"The operation has been completed successfully. Total images found: {total_images_found}")
        return
    app.after(100, check_thread)

# Create the main application window
app = tk.Tk()
app.title("SequenceCompressor")
app.geometry("800x600")

# Main frame
main_frame = tk.Frame(app)
main_frame.pack(padx=10, pady=10, fill='both', expand=True)

# Frame for selections and control buttons
selection_frame = tk.Frame(main_frame)
selection_frame.pack(fill='x')

# Entry for folder selection and folder selection button
folder_path_var = tk.StringVar()
folder_path_entry = tk.Entry(selection_frame, textvariable=folder_path_var, state='readonly', width=20)
folder_path_entry.pack(side='left', padx=(0, 10))
folder_select_button = tk.Button(selection_frame, text="Select Folder", command=select_folder)
folder_select_button.pack(side='left', padx=(0, 10))

# Dropdown menu to select image type
tk.Label(selection_frame, text="Image Type:").pack(side='left', padx=(10, 0))
extension_var = tk.StringVar()
extension_dropdown = ttk.Combobox(selection_frame, textvariable=extension_var, values=[".tga", ".png", ".ppm", ".tiff", ".gif", ".svg", ".dpx", ".exr", ".dng", ".jpg"])
extension_dropdown.pack(side='left')

# Button to start image compression
compress_button = tk.Button(selection_frame, text="Compress Images", command=start_compression)
compress_button.pack(side='right', padx=(0, 10))

# Button to start image decompression
decompress_button = tk.Button(selection_frame, text="Decompress Images", command=start_decompression)
decompress_button.pack(side='right')

# Button to save the report to a file
save_report_button = tk.Button(selection_frame, text="Save Report", command=save_log_to_file)
save_report_button.pack(side='right', padx=(10, 0))

# Frame for the text box to display reports and messages
log_frame = tk.Frame(main_frame)
log_frame.pack(fill='both', expand=True, pady=(10, 0))
log_text = scrolledtext.ScrolledText(log_frame, height=10)
log_text.pack(fill='both', expand=True)

# Frame for the progress bar
progress_frame = tk.Frame(main_frame)
progress_frame.pack(fill='x')

# Define progress variable and progress bar
progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(progress_frame, variable=progress_var, maximum=100, mode='determinate')
progress_bar.pack(fill='x', padx=10, pady=5)

app.mainloop()
