import os
import json
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import difflib

class Llsp3File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.python_code = None

    def extract_python_code(self):
        """Extracts Python code from a .llsp3 file."""
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                if "projectbody.json" in zip_ref.namelist():
                    with zip_ref.open("projectbody.json") as json_file:
                        project_data = json.load(json_file)
                        self.python_code = project_data.get("main", "")
        except zipfile.BadZipFile:
            messagebox.showerror("Error", f"{os.path.basename(self.filepath)} is not a valid ZIP archive.")
            return None
        return self.python_code

    def update_code(self, new_code):
        """Updates the .llsp3 file with the new Python code."""
        try:
            temp_zip = self.filepath + "_temp"
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                zip_ref.extractall(temp_zip)

            json_path = os.path.join(temp_zip, "projectbody.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                data["main"] = new_code
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, indent=4)

            with zipfile.ZipFile(self.filepath, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
                for root, _, files in os.walk(temp_zip):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zip_ref.write(file_path, os.path.relpath(file_path, temp_zip))

            for root, _, files in os.walk(temp_zip, topdown=False):
                for file in files:
                    os.remove(os.path.join(root, file))
                os.rmdir(root)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update .llsp3 file: {e}")

class GitMergeSimulator:
    def __init__(self, original_code, new_code):
        self.original_code = original_code.splitlines()
        self.new_code = new_code.splitlines()

    def merge(self):
        """Simulates a Git-like merge with conflict handling."""
        diff = list(difflib.ndiff(self.original_code, self.new_code))
        merged_lines = []
        conflict_detected = False

        for line in diff:
            if line.startswith("  "):  # Unchanged line
                merged_lines.append(line[2:])
            elif line.startswith("- "):  # Line removed in new version
                merged_lines.append(f"<<<<<<<< OLD VERSION\n{line[2:]}\n========")
                conflict_detected = True
            elif line.startswith("+ "):  # Line added in new version
                merged_lines.append(f"{line[2:]}\n>>>>>>>> NEW VERSION")
                conflict_detected = True

        if conflict_detected:
            return "\n".join(merged_lines)
        else:
            return "\n".join(merged_lines)

# Global variable to store the current Llsp3File being processed
current_llsp3_file = None

def convert_and_sync():
    """Handles file conversion and syncing with existing .py files."""
    global current_llsp3_file
    filepaths = filedialog.askopenfilenames(filetypes=[("LLSP3 Files", "*.llsp3")])
    if not filepaths:
        return

    for filepath in filepaths:
        current_llsp3_file = Llsp3File(filepath)
        new_python_code = current_llsp3_file.extract_python_code()
        if new_python_code is None:
            continue

        py_filename = os.path.splitext(os.path.basename(filepath))[0] + ".py"
        py_filepath = os.path.join(os.path.dirname(filepath), py_filename)

        if os.path.exists(py_filepath):
            with open(py_filepath, "r", encoding="utf-8") as py_file:
                existing_code = py_file.read()

            merge_tool = GitMergeSimulator(existing_code, new_python_code)
            merged_code = merge_tool.merge()

            with open(py_filepath, "w", encoding="utf-8") as py_file:
                py_file.write(merged_code)

            # Store the merged code temporarily in the current llsp3 file object
            current_llsp3_file.python_code = merged_code

        else:
            with open(py_filepath, "w", encoding="utf-8") as py_file:
                py_file.write(new_python_code)
            current_llsp3_file.update_code(new_python_code)

    messagebox.showinfo("Success", "Python files merged. Please review the changes.")

def finalize_and_push():
    """Finalize the merge and push the changes back to both the Python file and the .llsp3 archive."""
    global current_llsp3_file

    if current_llsp3_file and hasattr(current_llsp3_file, 'python_code') and current_llsp3_file.python_code:
        merged_code = current_llsp3_file.python_code
        py_filename = os.path.splitext(os.path.basename(current_llsp3_file.filepath))[0] + ".py"
        py_filepath = os.path.join(os.path.dirname(current_llsp3_file.filepath), py_filename)

        # Save merged code to the Python file.
        with open(py_filepath, "w", encoding="utf-8") as py_file:
            py_file.write(merged_code)

        # Now push the changes into the .llsp3 file.
        current_llsp3_file.update_code(merged_code)

        # Final Git commit and push after synchronization.
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
    else:
        messagebox.showerror("Error", "No merged code available for push.")

def setup_gui():
    """Sets up the Tkinter UI."""
    root = tk.Tk()
    root.title("LLSP3 Sync Tool")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack()

    tk.Button(frame, text="Convert & Sync .llsp3 to .py", command=convert_and_sync).pack(pady=5)

    global commit_entry
    commit_entry = tk.Entry(frame, width=50)
    commit_entry.pack(pady=5)
    commit_entry.insert(0, "Enter commit message")

    tk.Button(frame, text="Finalize & Push Changes", command=finalize_and_push).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_gui()
