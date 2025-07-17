import re

def scan_jwt(file_path):
    results = []
    jwt_pattern = r'eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if re.search(jwt_pattern, line):
                results.append({
                    "file": file_path,
                    "line": i,
                    "code": line.strip(),
                    "issue": "JWT token exposed in CSS file",
                    "fix": "Never store JWTs in CSS files. These are static and public.",
                    "language": "css"
                })
    except Exception as e:
        print(f"[ERROR] CSS JWT scan failed on {file_path}: {e}")

    return results
