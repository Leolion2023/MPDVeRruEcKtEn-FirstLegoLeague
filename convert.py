import os
import json
import zipfile

def extract_python_code_from_llsp3(directory):
    """Processes all .llsp3 files in the given directory and extracts Python code."""
    for filename in os.listdir(directory):
        if filename.endswith(".llsp3"):
            llsp3_path = os.path.join(directory, filename)
            py_filename = os.path.splitext(filename)[0] + ".py"
            py_filepath = os.path.join(directory, py_filename)
            
            try:
                with zipfile.ZipFile(llsp3_path, 'r') as zip_ref:
                    if "projectbody.json" in zip_ref.namelist():
                        with zip_ref.open("projectbody.json") as json_file:
                            project_data = json.load(json_file)
                            python_code = project_data.get("main", "")
                            
                            if python_code:
                                with open(py_filepath, "w", encoding="utf-8") as py_file:
                                    py_file.write(python_code)
                                print(f"Extracted: {py_filename}")
                            else:
                                print(f"No Python code found in {filename}.")
                    else:
                        print(f"No 'projectbody.json' found in {filename}.")
            except zipfile.BadZipFile:
                print(f"Error: {filename} is not a valid ZIP archive.")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    extract_python_code_from_llsp3(script_directory)
