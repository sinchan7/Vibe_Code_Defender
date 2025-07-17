def scan_unsafe_calls(file_path):
    results = []
    unsafe_functions = ["system(", "popen(", "gets(", "strcpy(", "sprintf("]

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            for func in unsafe_functions:
                if func in line:
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": f"Use of unsafe function `{func.strip('(')}`",
                        "fix": "Use safer alternatives like `fgets`, `strncpy`, or input validation.",
                        "language": "cpp"
                    })
    except Exception as e:
        print(f"[ERROR] Unsafe call scan failed on {file_path}: {e}")

    return results
