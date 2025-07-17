import re

def scan_secrets(file_path):
    results = []
    patterns = [
        (r'/\*.*?(apikey|token|secret).*?\*/', 'Possible secret in CSS comment'),
        (r'content\s*:\s*["\'].*?(apikey|token|secret).*?["\']', 'Possible secret exposed in content'),
    ]

    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines, 1):
            for pattern, issue in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    results.append({
                        "file": file_path,
                        "line": i,
                        "code": line.strip(),
                        "issue": issue,
                        "fix": "Avoid storing secrets or tokens in CSS. These are publicly accessible.",
                        "language": "css"
                    })
    except Exception as e:
        print(f"[ERROR] CSS secret scan failed on {file_path}: {e}")

    return results
