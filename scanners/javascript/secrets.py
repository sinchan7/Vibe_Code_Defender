import re

def scan_secrets(file_path):
    results = []
    patterns = [
        (r'(?i)(api[_-]?key\s*[:=]\s*[\'"][a-z0-9]{16,}[\'"])', 'Possible API key hardcoded'),
        (r'(?i)(secret\s*[:=]\s*[\'"][^\'"]+[\'"])', 'Possible secret hardcoded'),
        (r'(?i)(password\s*[:=]\s*[\'"][^\'"]+[\'"])', 'Possible password hardcoded'),
    ]

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            for pattern, issue in patterns:
                if re.search(pattern, line):
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": issue,
                        "fix": "Move secret values to environment variables or config files.",
                        "language": "javascript"
                    })
    except Exception as e:
        print(f"[ERROR] Secret scan failed on {file_path}: {e}")

    return results
