import re

DANGEROUS_HTML_PATTERNS = [
    {
        "pattern": r"<script[^>]*?>.*?</script>",
        "issue": "Inline <script> tags can allow XSS attacks.",
        "fix": "Move scripts to external files and use CSP headers.",
        "severity": "High"
    },
    {
        "pattern": r"<form[^>]*?>",
        "issue": "Forms without proper 'action' or 'method' attributes can be vulnerable.",
        "fix": "Use 'action' and 'method' attributes explicitly in forms.",
        "severity": "Medium"
    },
    {
        "pattern": r"\son\w+\s*=",
        "issue": "Inline event handlers (like onclick) can lead to DOM XSS.",
        "fix": "Use addEventListener in external JS files instead.",
        "severity": "Medium"
    },
    {
        "pattern": r"<iframe[^>]+src=",
        "issue": "Untrusted iframes can embed malicious content.",
        "fix": "Avoid using iframes or use sandboxing attributes.",
        "severity": "Medium"
    },
    {
        "pattern": r"<meta[^>]+http-equiv=['\"]Content-Security-Policy['\"]",
        "issue": "Missing Content-Security-Policy meta tag.",
        "fix": "Add a meta CSP tag to restrict inline scripts.",
        "severity": "Low"
    }
]

def scan_files(file_list):
    findings = []

    for file_path in file_list:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

            for idx, line in enumerate(lines, start=1):
                for rule in DANGEROUS_HTML_PATTERNS:
                    if re.search(rule["pattern"], line, flags=re.IGNORECASE):
                        findings.append({
                            "file": file_path,
                            "line": idx,
                            "code": line.strip(),
                            "issue": rule["issue"],
                            "fix": rule["fix"],
                            "severity": rule["severity"],
                            "language": "html"
                        })

        except Exception as e:
            print(f"[HTML Scanner] Error in {file_path}: {e}")

    return findings
