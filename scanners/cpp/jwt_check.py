def scan_jwt(file_path):
    results = []

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if "jwt" in line.lower() and ("none" in line.lower() or "algorithm" in line.lower()):
                results.append({
                    "file": file_path,
                    "line": i,
                    "code": line.strip(),
                    "issue": "Potential weak JWT algorithm or insecure implementation",
                    "fix": "Ensure JWT uses secure algorithms (e.g., HS256, RS256) and is properly verified.",
                    "language": "cpp"
                })
    except Exception as e:
        print(f"[ERROR] JWT scan failed on {file_path}: {e}")

    return results
