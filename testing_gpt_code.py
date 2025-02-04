#!/usr/bin/env python3
import difflib
import zipfile
import os
from tkinter import messagebox
import json


class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.python_code: str = None
        self.raw_code = None
        self.merged_code: str = None

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

    def update_code(self, new_code: str):
        pass


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
                        zip_ref.write(file_path, os.path.relpath(
                            file_path, temp_zip))

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

    def update_code(self, new_code: str):
        """Updates the .py file with the new Python code."""
        try:
            with open(self.filepath, "w", encoding="utf-8") as py_file:
                py_file.write(new_code)
        except Exception as e:
            messagebox.showerror("Error", "Failed to update {}.py file: {}".format(
                os.path.basename(self.filepath), e))


def build_change_map(base, side):
    """
    Build a change map that represents the transformation from the base to one side.
    
    The change map is a dict mapping a base index (from 0 to len(base)) to a dictionary
    that can have two keys:
      - 'insert': a list of lines inserted at that base index (i.e. before base[i])
      - 'replace': a list of lines that replace the base line at that index.
      
    For an insertion, the base index i means “insert before base[i]”. Note that insertions
    at index len(base) are after the last line.
    
    We use difflib.SequenceMatcher to compute opcodes (which tell us what regions differ).
    """
    matcher = difflib.SequenceMatcher(None, base, side)
    opcodes = matcher.get_opcodes()
    changes = {}
    for tag, i1, i2, j1, j2 in opcodes:
        if tag == 'equal':
            continue
        if tag == 'insert':
            # Insertion at base index i1 (i1 == i2)
            changes.setdefault(i1, {})
            changes[i1].setdefault('insert', []).extend(side[j1:j2])
        elif tag in ('replace', 'delete'):
            # For a replacement or deletion, we “attach” the changed text
            # to the first base line in the changed region.
            changes.setdefault(i1, {})
            changes[i1]['replace'] = side[j1:j2]
    return changes

def merge_insertions(local_ins, remote_ins):
    """
    Merge two lists of inserted lines (from local and remote) at the same base index.
    
    - If both sides inserted text and the inserted blocks are identical, return them.
    - If both sides inserted text but they differ, return a conflict block.
    - If only one side inserted text, return that insertion.
    """
    if local_ins and remote_ins:
        if local_ins == remote_ins:
            return local_ins
        else:
            return (
                ["<<<<<<< LOCAL\n"]
                + local_ins
                + ["=======\n"]
                + remote_ins
                + [">>>>>>> REMOTE\n"]
            )
    elif local_ins:
        return local_ins
    elif remote_ins:
        return remote_ins
    else:
        return []

def merge_three_way(base, local, remote):
    """
    Perform a three-way merge of the sequences of lines: base, local, and remote.
    
    For each position in the base (from index 0 up to len(base)):
      1. Merge any insertions at that position.
      2. If there is a change on the base line itself (a replacement) then:
         - If only one side replaced, use that.
         - If both sides replaced and the replacements are identical, use that.
         - If both sides replaced but the replacements differ, output a conflict block.
      3. If neither side replaced the base line, output the base line.
      
    Returns a list of lines representing the merged result.
    """
    # Build change maps from base to local and base to remote.
    local_changes = build_change_map(base, local)
    remote_changes = build_change_map(base, remote)
    
    merged = []
    n = len(base)
    # Iterate from index 0 to n (where index n means “after the last line”)
    for i in range(n + 1):
        # 1. Process any insertions at this base position.
        local_ins = local_changes.get(i, {}).get('insert', [])
        remote_ins = remote_changes.get(i, {}).get('insert', [])
        merged.extend(merge_insertions(local_ins, remote_ins))
        
        # 2. If i < n, then process the base line at i.
        if i < n:
            local_rep = local_changes.get(i, {}).get('replace', None)
            remote_rep = remote_changes.get(i, {}).get('replace', None)
            
            # No replacement: use the base line.
            if local_rep is None and remote_rep is None:
                merged.append(base[i])
            # Only one side changed: use that change.
            elif local_rep is not None and remote_rep is None:
                merged.extend(local_rep)
            elif local_rep is None and remote_rep is not None:
                merged.extend(remote_rep)
            else:
                # Both sides replaced the base line.
                if local_rep == remote_rep:
                    merged.extend(local_rep)
                else:
                    merged.append("<<<<<<< LOCAL\n")
                    merged.extend(local_rep)
                    merged.append("=======\n")
                    merged.extend(remote_rep)
                    merged.append(">>>>>>> REMOTE\n")
    return merged

# === Example Usage ===

if __name__ == "__main__":
    # Example input files as lists of lines (each line ends with a newline)
    base = PythonFile("base.py").extract_python_code().splitlines(keepends=True)
    local = PythonFile("local.py").extract_python_code().splitlines(keepends=True)
    remote = PythonFile("remote.py").extract_python_code().splitlines(keepends=True)

    
    merged_result = merge_three_way(base, local, remote)
    
    # Output the merged result
    output = PythonFile("merged.py")
    output.update_code("".join(merged_result))
