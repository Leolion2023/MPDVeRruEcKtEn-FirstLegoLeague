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
        self.merged_code = None
        self.llsp3_data = None

    def extract_python_code(self):
        """Extracts Python code from a .llsp3 file."""
        try:
            with zipfile.ZipFile(self.filepath, 'r') as zip_ref:
                if "projectbody.json" in zip_ref.namelist():
                    with zip_ref.open("projectbody.json") as json_file:
                        project_data = json.load(json_file)
                        self.python_code = project_data.get("main", "")
                        self.llsp3_data = project_data  # Store the entire JSON data for further use
                        self.merged_code = self.python_code  # Store the initial code for merging
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
                data["main"] = new_code  # Update the Python code
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
    
def extract_python_from_llsp3bytes(llsp3_bytes):
    """Extract Python code from a binary llsp3 file."""
    try:
        # Write bytes to a temporary ZIP file
        temp_file = "temp_llsp3.zip"
        with open(temp_file, "wb") as f:
            f.write(llsp3_bytes)

        # Open ZIP and extract projectbody.json
        with zipfile.ZipFile(temp_file, "r") as zip_ref:
            if "projectbody.json" in zip_ref.namelist():
                with zip_ref.open("projectbody.json") as json_file:
                    project_data = json.load(json_file)
                    return project_data.get("main", "")

    except zipfile.BadZipFile:
        print("Error: The provided .llsp3 data is not a valid ZIP archive.")
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)  # Clean up temp file

    return None


class GitMergeSimulator:
    def __init__(self, original_code, new_code):
        self.original_code = original_code.splitlines()
        self.new_code = new_code.splitlines()

    def merge(self):
        """Simulates a Git-like merge with conflict handling."""
        diff = list(difflib.ndiff(self.original_code, self.new_code))
        print(diff)
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


def fetch_git_py(filepath, version):
    """Fetch the Git version of a file (base, current, or other), using the filename only."""
    try:
        # Get the root directory of the Git repository
        git_root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], 
            capture_output=True, 
            check=True, 
            text=False  # Avoid automatic decoding of output
        ).stdout
        print(filepath)

        # Extract the filename from the full path
        filename = os.path.basename(filepath)

        # Construct the relative path for the file from the Git root directory
        relative_filepath = os.path.relpath(filepath, git_root.decode("utf-8").strip())

        # Fetch the specific version from Git using the relative file path
        result = subprocess.run(
            ["git", "show", f"{version}:{relative_filepath}"], 
            capture_output=True, 
            check=True, 
            text=False  # Avoid automatic decoding of output
        )

        # Explicitly decode the output if needed
        return result.stdout.decode("utf-8", errors="replace")  # Use 'replace' to handle undecodable chars
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Git Error", f"Failed to fetch Git version: {e}")
        return None

def fetch_git_llsp3(filepath, version):
    """Fetch a file's version from Git and return its contents as bytes."""
    try:
        # Get the relative path in the Git repo
        git_root = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, check=True, text=True).stdout.strip()
        relative_filepath = os.path.relpath(filepath, git_root)

        # Fetch the file's contents from Git
        result = subprocess.run(["git", "show", f"{version}:{relative_filepath}"], capture_output=True, check=True)

        return extract_python_from_llsp3bytes(result.stdout)
    except Exception as e:
        print(f"Git error: {e}")
        raise e


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

            # First, fetch the Git versions of both the .py and .llsp3 files
            base_python_code = fetch_git_py(py_filepath, "HEAD")
            base_llsp3_code = fetch_git_llsp3(filepath, "HEAD")

            # Compare the base versions of the files with the current ones
            if base_python_code and base_llsp3_code:
                # Compare the Python code versions
                merge_tool = GitMergeSimulator(existing_code, new_python_code)
                merged_code = merge_tool.merge()

                # Convert the .llsp3 file and compare its versions
                llsp3_merge_tool = GitMergeSimulator(base_llsp3_code, new_python_code)
                merged_llsp3_code = llsp3_merge_tool.merge()

                # Update both files if changes exist
                current_llsp3_file.update_code(merged_llsp3_code)
                with open(py_filepath, "w", encoding="utf-8") as py_file:
                    py_file.write(merged_code)
            else:
                messagebox.showerror("Git Error", "Failed to fetch base Git versions.")
        else:
            print("File not used")

    messagebox.showinfo("Success", "Python files merged. Please review the changes.")


def finalize_and_push():
    """Finalize the merge and push the changes back to both the Python file and the .llsp3 archive."""
    global current_llsp3_file

    if current_llsp3_file:
        # Check if the Python file was manually changed after merge
        py_filename = os.path.splitext(os.path.basename(current_llsp3_file.filepath))[0] + ".py"
        py_filepath = os.path.join(os.path.dirname(current_llsp3_file.filepath), py_filename)

        with open(py_filepath, "r", encoding="utf-8") as py_file:
            user_modified_code = py_file.read()

        # If user modified the Python file, use it instead of the merged code
        if user_modified_code != current_llsp3_file.merged_code:
            merged_code = user_modified_code
        else:
            merged_code = current_llsp3_file.merged_code

        # Update the .llsp3 file with the final code (whether it's the merged code or user's manual change)
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
            messagebox.showerror("Git Error", f"Failed to commit and push changes: {e}")
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
