def scan_jwt(file_path):
    results = []

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if "jwt." in line and (".sign" in line or ".verify" in line):
                if "none" in line.lower() or "'none'" in line or '"none"' in line:
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": "JWT algorithm set to 'none'",
                        "fix": "Use a secure algorithm like HS256 or RS256.",
                        "language": "javascript"
                    })
    except Exception as e:
        print(f"[ERROR] JWT scan failed on {file_path}: {e}")

    return results
