def scan_unsafe_calls(file_path):
    results = []
    unsafe_functions = ["eval", "Function", "setTimeout", "setInterval", "execScript"]

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            for func in unsafe_functions:
                if f"{func}(" in line:
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": f"Use of dangerous function `{func}`",
                        "fix": f"Avoid using `{func}`. Consider alternatives or proper sanitization.",
                        "language": "javascript"
                    })
    except Exception as e:
        print(f"[ERROR] Unsafe call scan failed on {file_path}: {e}")

    return results
