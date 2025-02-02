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