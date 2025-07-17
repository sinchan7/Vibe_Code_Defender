import re

def scan_unsafe_calls(file_path):
    results = []
    pattern = r'expression\s*\('  # legacy IE only, used for XSS

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            if re.search(pattern, line, re.IGNORECASE):
                results.append({
                    "file": file_path,
                    "line": i,
                    "code": line.strip(),
                    "issue": "Use of `expression()` is insecure and deprecated",
                    "fix": "Remove `expression()` usage. It is a security risk.",
                    "language": "css"
                })
    except Exception as e:
        print(f"[ERROR] CSS unsafe call scan failed on {file_path}: {e}")

    return results
