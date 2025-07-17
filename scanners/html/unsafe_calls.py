import re

def scan_unsafe_calls(file_path):
    results = []
    patterns = [
        (r'onerror\s*=', 'Use of inline `onerror` event handler, potential XSS'),
        (r'onload\s*=', 'Use of inline `onload` event handler, potential XSS'),
        (r'<script[^>]*>.*document\.write\(', 'Use of `document.write()` can lead to XSS'),
        (r'<script[^>]*>.*innerHTML\s*=', 'Assignment to `innerHTML` can lead to XSS'),
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
                        "fix": "Avoid unsafe JavaScript practices inside HTML. Sanitize inputs.",
                        "language": "html"
                    })
    except Exception as e:
        print(f"[ERROR] HTML unsafe call scan failed on {file_path}: {e}")

    return results
