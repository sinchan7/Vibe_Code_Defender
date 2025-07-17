def scan_jwt(file_path):
    results = []

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if "JWT" in line and ("setAlgorithm" in line or "signWith" in line):
                if "none" in line.lower():
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": "JWT algorithm set to 'none'",
                        "fix": "Use a secure algorithm like HS256 or RS256.",
                        "language": "java"
                    })
    except Exception as e:
        print(f"[ERROR] JWT scan failed on {file_path}: {e}")

    return results
