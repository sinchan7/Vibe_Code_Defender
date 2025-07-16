import os
import re

SECRET_PATTERNS = [
    (r'API_KEY\s*=\s*["\'].*["\']', "Hardcoded API key"),
    (r'(?i)secret\s*=\s*["\'].*["\']', "Hardcoded secret"),
    (r'(?i)token\s*=\s*["\'].*["\']', "Hardcoded token"),
]

FIX_SUGGESTION = (
    "Move this value to a `.env` file and access it using `os.getenv()`.\n"
    "Example:\n```python\nAPI_KEY = os.getenv('API_KEY')\n```"
)

def scan_secrets(base_path):
    results = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, 'r', errors='ignore') as f:
                    lines = f.readlines()
                    for idx, line in enumerate(lines):
                        for pattern, message in SECRET_PATTERNS:
                            if re.search(pattern, line):
                                results.append({
                                    "file": path,
                                    "line": idx + 1,
                                    "issue": message,
                                    "code": line.strip(),
                                    "fix": FIX_SUGGESTION
                                })
    return results
