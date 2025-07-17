import re

def scan_secrets(file_path):
    results = []
    patterns = [
        (r'(?i)(const\s+char\s*\*\s*(api[_-]?key|secret|token|password)\s*=\s*"[^"]+")', 'Hardcoded secret detected'),
        (r'(?i)(std::string\s+(api[_-]?key|secret|token|password)\s*=\s*"[^"]+")', 'Hardcoded secret detected'),
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
                        "fix": "Avoid hardcoding secrets. Use secure config or environment variables.",
                        "language": "cpp"
                    })
    except Exception as e:
        print(f"[ERROR] Secret scan failed on {file_path}: {e}")

    return results
