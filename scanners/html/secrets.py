import re

def scan_secrets(file_path):
    results = []
    patterns = [
        (r'<script[^>]*>.*?(apikey|token|secret).*?=.*?["\'].*?["\']', 'Possible hardcoded secret in script tag'),
        (r'<meta[^>]+(apikey|token|secret)[^>]*>', 'Possible secret exposed in meta tag'),
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
                        "fix": "Do not expose secrets in HTML. Use secure backend APIs.",
                        "language": "html"
                    })
    except Exception as e:
        print(f"[ERROR] HTML secret scan failed on {file_path}: {e}")

    return results
