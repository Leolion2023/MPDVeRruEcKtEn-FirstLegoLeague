import os
import json
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import difflib

def extract_python_code_from_llsp3(filepath):
    """Extracts Python code from a .llsp3 file."""
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            if "projectbody.json" in zip_ref.namelist():
                with zip_ref.open("projectbody.json") as json_file:
                    project_data = json.load(json_file)
                    return project_data.get("main", "")
    except zipfile.BadZipFile:
        messagebox.showerror("Error", f"{os.path.basename(filepath)} is not a valid ZIP archive.")
    return None

def convert_and_save():
    """Handles file conversion from .llsp3 to .py."""
    filepaths = filedialog.askopenfilenames(filetypes=[("LLSP3 Files", "*.llsp3")])
    if not filepaths:
        return
    
    converted_files = []
    for filepath in filepaths:
        python_code = extract_python_code_from_llsp3(filepath)
        if python_code is not None:
            py_filename = os.path.splitext(os.path.basename(filepath))[0] + ".py"
            py_filepath = os.path.join(os.path.dirname(filepath), py_filename)
            with open(py_filepath, "w", encoding="utf-8") as py_file:
                py_file.write(python_code)
            converted_files.append(py_filepath)
    
    if converted_files:
        messagebox.showinfo("Success", "Conversion completed successfully!")

def commit_and_push():
    """Handles Git commit and push operations."""
    commit_message = commit_entry.get()
    if not commit_message:
        messagebox.showerror("Error", "Commit message cannot be empty.")
        return
    
    try:
        subprocess.run(["git", "add", "-A"], check=True)
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push"], check=True)
        messagebox.showinfo("Success", "Changes committed and pushed successfully!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Git Error", f"Git command failed: {e}")

def merge_files(original_path, new_path):
    """Compares two Python files and merges them."""
    with open(original_path, "r", encoding="utf-8") as f1, open(new_path, "r", encoding="utf-8") as f2:
        original_lines = f1.readlines()
        new_lines = f2.readlines()
    
    merged_lines = list(difflib.unified_diff(original_lines, new_lines, lineterm=""))
    if not merged_lines:
        return
    
    merge_result = "".join(merged_lines)
    conflict_file = os.path.splitext(original_path)[0] + "_merged.py"
    with open(conflict_file, "w", encoding="utf-8") as f:
        f.write(merge_result)
    
    messagebox.showinfo("Merge Conflict", f"Conflicts found. Merged file saved as {conflict_file}")

def merge_tool():
    """Handles merging logic for updated .py files."""
    filepaths = filedialog.askopenfilenames(filetypes=[("Python Files", "*.py")])
    if len(filepaths) != 2:
        messagebox.showerror("Error", "Please select exactly two Python files to compare.")
        return
    
    merge_files(filepaths[0], filepaths[1])

def setup_gui():
    """Sets up the Tkinter UI."""
    root = tk.Tk()
    root.title("LLSP3 Converter & Git Manager")
    
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()
    
    tk.Button(frame, text="Convert .llsp3 to .py", command=convert_and_save).pack(pady=5)
    
    global commit_entry
    commit_entry = tk.Entry(frame, width=50)
    commit_entry.pack(pady=5)
    commit_entry.insert(0, "Enter commit message")
    
    tk.Button(frame, text="Commit & Push", command=commit_and_push).pack(pady=5)
    tk.Button(frame, text="Merge Tool", command=merge_tool).pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
