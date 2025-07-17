def scan_unsafe_calls(file_path):
    results = []
    unsafe_functions = ["Runtime.getRuntime().exec", "ProcessBuilder", "eval", "ScriptEngineManager"]

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
                        "issue": f"Use of dangerous function `{func}`",
                        "fix": f"Avoid using `{func}` directly. Validate inputs and consider safer alternatives.",
                        "language": "java"
                    })
    except Exception as e:
        print(f"[ERROR] Unsafe call scan failed on {file_path}: {e}")

    return results
