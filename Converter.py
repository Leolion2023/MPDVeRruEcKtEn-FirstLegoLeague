import os
import json
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import subprocess
import difflib


class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.python_code: str = None
        self.raw_code = None

    def extract_python_code(self):
        """Extracts Python code from a file."""
        if os.path.splitext(self.filepath)[1] == ".py":
            with open(self.filepath, "r", encoding="utf-8") as py_file:
                data = py_file.read()
                self.python_code = data
                self.raw_code = data
                return data
        try:
            with zipfile.ZipFile(self.filepath, "r") as zip_ref:
                if "projectbody.json" in zip_ref.namelist():
                    with zip_ref.open("projectbody.json") as json_file:
                        project_data = json.load(json_file)
                        self.python_code = project_data.get("main", "")
                        self.raw_code = project_data
        except zipfile.BadZipFile:
            messagebox.showerror(
                "Error",
                f"{os.path.basename(self.filepath)} is not a valid ZIP archive.",
            )
            return None
        return self.python_code


class llsp3File(File):
    def extract_python_code(self) -> str:
        """Extracts Python code from a .llsp3 file."""
        try:
            with zipfile.ZipFile(self.filepath, "r") as zip_ref:
                if "projectbody.json" in zip_ref.namelist():
                    with zip_ref.open("projectbody.json") as json_file:
                        project_data = json.load(json_file)
                        self.python_code = project_data.get("main", "")
        except zipfile.BadZipFile:
            messagebox.showerror(
                "Error",
                f"{os.path.basename(self.filepath)} is not a valid ZIP archive.",
            )
            return None
        return self.python_code

    def write_binary(self, llsp3_bytes):
        """Write binary data to filepath of File"""
        try:
            with open(self.filepath, "wb") as file:
                file.write(llsp3_bytes)
                self.raw_code = llsp3_bytes
        except:
            raise

    def update_code(self, new_code):
        """Updates the .llsp3 file with the new Python code."""
        try:
            temp_zip = self.filepath + "_temp"
            with zipfile.ZipFile(self.filepath, "r") as zip_ref:
                zip_ref.extractall(temp_zip)

            json_path = os.path.join(temp_zip, "projectbody.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as json_file:
                    data = json.load(json_file)
                data["main"] = new_code  # Update the Python code
                with open(json_path, "w", encoding="utf-8") as json_file:
                    json.dump(data, json_file, indent=4)

            with zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED) as zip_ref:
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


class PythonFile(File):
    def extract_python_code(self):
        """Extracts Python code from a py file."""
        if os.path.splitext(self.filepath)[1] == ".py":
            with open(self.filepath, "r", encoding="utf-8") as py_file:
                data = py_file.read()
                self.python_code = data
                return data

    def update_code(self, new_code):
        """Updates the .py file with the new Python code."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as py_file:
                py_file.write(new_code)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update .py file: {e}")


class GitTool:
    def __init__(self, llsp3_file: llsp3File, python_file: PythonFile):
        self.llsp3_file = llsp3_file
        self.python_file = python_file

    def global_merge(self):
        """Merge the different filetypes together"""
        pass

    def python_merge(self):
        """Merge the pythonfile with the HEAD git code"""
        python_path = self.python_file.filepath
        base_lines = []
        remote_lines = []

        try:
            base = self.__fetch_python__(python_path, self.__get_base_version__(python_path))
            base_lines = base.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch base version: {e}")

        try:
            remote = self.__fetch_python__(python_path, "origin/main")
            remote_lines = remote.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch remote version: {e}")

        local = self.python_file.extract_python_code()
        local_lines = local.splitlines()

        merged_lines = []
        conflict = False

        sm_local = difflib.SequenceMatcher(None, base_lines, local_lines, False)
        sm_remote = difflib.SequenceMatcher(None, base_lines, remote_lines)

        local_changes = {}
        remote_changes = {}

        for tag, i1, i2, j1, j2 in sm_local.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(local_lines[j1:j2]):
                        local_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        local_changes[i] = [""]

        for tag, i1, i2, j1, j2 in sm_remote.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(remote_lines[j1:j2]):
                        remote_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        remote_changes[i] = [""]
        
        max_len = max(len(base_lines), max(local_changes.keys(), default=0) + 1, max(remote_changes.keys(), default=0) + 1)

        for i in range(max_len):
            base_line = base_lines[i] if i < len(base_lines) else ""
            local_change = local_changes.get(i, [base_line])
            remote_change = remote_changes.get(i, [base_line])
            
            if local_change == remote_change:
                merged_lines.extend(local_change)
            elif local_change != [base_line] and remote_change != [base_line]:
                conflict = True
                merged_lines.append(f"<<<<<<< LOCAL\n" + "\n".join(local_change) +
                                    "\n=======\n" + "\n".join(remote_change) +
                                    "\n>>>>>>> REMOTE")
            elif local_change != [base_line]:
                merged_lines.extend(local_change)
            elif remote_change != [base_line]:
                merged_lines.extend(remote_change)
            else:
                merged_lines.append(base_line)

        if conflict:
            print("Merge conflict detected. Manual resolution required.")
            output_file = PythonFile("merged_code.py")
            output_file.update_code("\n".join(merged_lines))
        else:
            print("No conflicts detected. Merging successful.")

        return "\n".join(merged_lines)




    def llsp3_merge(self):
        """Merge the llsp3file with the HEAD git code"""

        llsp3path = self.llsp3_file.filepath
        base_lines = []
        remote_lines = []

        try:
            base_raw = self.__fetch_llsp3__(llsp3path, self.__get_base_version__(llsp3path))
            base_llsp3 = llsp3File("base.llsp3")
            base_llsp3.write_binary(base_raw)
            base = base_llsp3.extract_python_code()
            base_lines = base.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch base version: {e}")

        try:
            remote_raw = self.__fetch_llsp3__(llsp3path, "origin/main")
            remote_llsp3 = llsp3File("remote.llsp3")
            remote_llsp3.write_binary(remote_raw)
            remote = remote_llsp3.extract_python_code()
            remote_lines = remote.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch remote version: {e}")

        local = self.llsp3_file.extract_python_code()
        local_lines = local.splitlines()

        merged_lines = []
        conflict = False

        sm_local = difflib.SequenceMatcher(None, base_lines, local_lines, False)
        sm_remote = difflib.SequenceMatcher(None, base_lines, remote_lines)

        local_changes = {}
        remote_changes = {}

        for tag, i1, i2, j1, j2 in sm_local.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(local_lines[j1:j2]):
                        local_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        local_changes[i] = [""]

        for tag, i1, i2, j1, j2 in sm_remote.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(remote_lines[j1:j2]):
                        remote_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        remote_changes[i] = [""]
        
        max_len = max(len(base_lines), max(local_changes.keys(), default=0) + 1, max(remote_changes.keys(), default=0) + 1)

        for i in range(max_len):
            base_line = base_lines[i] if i < len(base_lines) else ""
            local_change = local_changes.get(i, [base_line])
            remote_change = remote_changes.get(i, [base_line])
            
            if local_change == remote_change:
                merged_lines.extend(local_change)
            elif local_change != [base_line] and remote_change != [base_line]:
                conflict = True
                merged_lines.append(f"<<<<<<< LOCAL\n" + "\n".join(local_change) +
                                    "\n=======\n" + "\n".join(remote_change) +
                                    "\n>>>>>>> REMOTE")
            elif local_change != [base_line]:
                merged_lines.extend(local_change)
            elif remote_change != [base_line]:
                merged_lines.extend(remote_change)
            else:
                merged_lines.append(base_line)

        if conflict:
            print("Merge conflict detected. Manual resolution required.")
            output_file = PythonFile("merged_code.py")
            output_file.update_code("\n".join(merged_lines))

        if os.path.exists(base_llsp3.filepath):
            os.remove(base_llsp3.filepath)
        if os.path.exists(remote_llsp3.filepath):
            os.remove(remote_llsp3.filepath)

        return "\n".join(merged_lines)

    def test_merge(self):
        llsp3path = self.llsp3_file.filepath
        base_lines = []
        remote_lines = []

        try:
            base_raw = self.__fetch_llsp3__(llsp3path, self.__get_base_version__(llsp3path))
            base_llsp3 = llsp3File("base.llsp3")
            base_llsp3.write_binary(base_raw)
            base = base_llsp3.extract_python_code()
            base_lines = base.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch base version: {e}")

        try:
            remote_raw = self.__fetch_llsp3__(llsp3path, "origin/main")
            remote_llsp3 = llsp3File("remote.llsp3")
            remote_llsp3.write_binary(remote_raw)
            remote = remote_llsp3.extract_python_code()
            remote_lines = remote.splitlines()
        except subprocess.CalledProcessError as e:
            print(f"Failed to fetch remote version: {e}")

        local = self.llsp3_file.extract_python_code()
        local_lines = local.splitlines()

        print("LOCAL\n")
        print(local_lines)

        merged_lines = []
        conflict = False

        sm_local = difflib.SequenceMatcher(None, base_lines, local_lines, False)
        sm_remote = difflib.SequenceMatcher(None, base_lines, remote_lines)

        local_changes = {}
        remote_changes = {}

        for tag, i1, i2, j1, j2 in sm_local.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                print('{:7}   base[{}:{}] --> local[{}:{}] {!r:>8} --> {!r}'.format(
                    tag, i1, i2, j1, j2, base_lines[i1:i2], local_lines[j1:j2]))
                
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(local_lines[j1:j2]):
                        local_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        local_changes[i] = [""]

        for tag, i1, i2, j1, j2 in sm_remote.get_opcodes():
            if tag in ("replace", "insert", "delete"):
                print('{:7}   base[{}:{}] --> local[{}:{}] {!r:>8} --> {!r}'.format(
                    tag, i1, i2, j1, j2, base_lines[i1:i2], remote_lines[j1:j2]))
                
                if tag == "replace" or tag == "insert":
                    for i, line in enumerate(remote_lines[j1:j2]):
                        remote_changes[i1 + i] = [line]
                elif tag == "delete":
                    for i in range(i1, i2):
                        remote_changes[i] = [""]

        print("LOCAL CHANGES\n")
        print(local_changes)
        print("REMOTE CHANGES\n")
        print(remote_changes)

        max_len = max(len(base_lines), max(local_changes.keys(), default=0) + 1, max(remote_changes.keys(), default=0) + 1)

        for i in range(max_len):
            base_line = base_lines[i] if i < len(base_lines) else ""
            local_change = local_changes.get(i, [base_line])
            remote_change = remote_changes.get(i, [base_line])
            
            if local_change == remote_change:
                print("No change detected: {}".format(base_line))
                merged_lines.extend(local_change)
            elif local_change != [base_line] and remote_change != [base_line]:
                conflict = True
                merged_lines.append(f"<<<<<<< LOCAL\n" + "\n".join(local_change) +
                                    "\n=======\n" + "\n".join(remote_change) +
                                    "\n>>>>>>> REMOTE")
            elif local_change != [base_line]:
                print("Local change detected: {}".format(local_change))
                merged_lines.extend(local_change)
            elif remote_change != [base_line]:
                print("Remote change detected: {}".format(remote_change))
                merged_lines.extend(remote_change)
            else:
                print("No change detected: {}".format(base_line))
                merged_lines.append(base_line)

        if conflict:
            print("Merge conflict detected. Manual resolution required.")

        if os.path.exists(base_llsp3.filepath):
            os.remove(base_llsp3.filepath)
        if os.path.exists(remote_llsp3.filepath):
            os.remove(remote_llsp3.filepath)

        output_file = PythonFile("merged_code.py")
        output_file.update_code("\n".join(merged_lines))

        return "\n".join(merged_lines)

    def __fetch_llsp3__(self, path, version="HEAD"):
        try:
            # Get the relative path in the Git repo
            git_root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                check=True,
                text=True,
            ).stdout.strip()
            relative_filepath = os.path.relpath(path, git_root)

            # Fetch the file's contents from Git
            result = subprocess.run(
                ["git", "show", "{}:{}".format(version, relative_filepath)],
                capture_output=True,
                check=True,
            )
            return result.stdout
        except Exception as e:
            print(f"Git error: {e}")
            raise

    def __fetch_python__(self, path, version="HEAD"):
        """Fetch the Git version of a file (base, current, or other), using the filename only."""
        try:
            # Get the root directory of the Git repository
            git_root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                check=True,
                text=False,  # Avoid automatic decoding of output
            ).stdout
            # Construct the relative path for the file from the Git root directory
            relative_filepath = os.path.relpath(path, git_root.decode("utf-8").strip())

            # Fetch the specific version from Git using the relative file path
            result = subprocess.run(
                ["git", "show", "{}:{}".format(version, relative_filepath)],
                capture_output=True,
                check=True,
                text=False,  # Avoid automatic decoding of output
            )
            # Explicitly decode the output if needed
            return result.stdout.decode(
                "utf-8", errors="replace"
            )  # Use 'replace' to handle undecodable chars
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Git Error", f"Failed to fetch Git version: {e}")
            return None
        
    def __get_base_version__(self, filepath):
        base_commit = subprocess.check_output(
            ["git", "merge-base", "HEAD", "origin/main"]
        ).decode().strip()
        return base_commit


def convert_and_sync():
    """Handles file conversion and syncing with existing .py files."""
    filepaths = filedialog.askopenfilenames(filetypes=[("LLSP3 Files", "*.llsp3")])
    if not filepaths:
        return

    for filepath in filepaths:
        llsp3_file = llsp3File(filepath)

        py_filename = os.path.splitext(os.path.basename(filepath))[0] + ".py"
        py_filepath = os.path.join(os.path.dirname(filepath), py_filename)

        py_file = PythonFile(py_filepath)
        new_llsp3python_code = llsp3_file.extract_python_code()
        if new_llsp3python_code is None:
            continue
        git_merger = GitTool(llsp3_file, py_file)

        git_merger.python_merge()

        # py_file.update_code(llsp3_file.extract_python_code())

    messagebox.showinfo("Success", "Python files merged. Please review the changes.")


def finalize_and_push():
    """Finalize the merge and push the changes back to both the Python file and the .llsp3 archive."""
    global current_llsp3_file

    if current_llsp3_file:
        # Check if the Python file was manually changed after merge
        py_filename = (
            os.path.splitext(os.path.basename(current_llsp3_file.filepath))[0] + ".py"
        )
        py_filepath = os.path.join(
            os.path.dirname(current_llsp3_file.filepath), py_filename
        )

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

    tk.Button(
        frame, text="Convert & Sync .llsp3 to .py", command=convert_and_sync
    ).pack(pady=5)

    global commit_entry
    commit_entry = tk.Entry(frame, width=50)
    commit_entry.pack(pady=5)
    commit_entry.insert(0, "Enter commit message")

    tk.Button(frame, text="Finalize & Push Changes", command=finalize_and_push).pack(
        pady=5
    )

    root.mainloop()


if __name__ == "__main__":
    setup_gui()
