import re

DANGEROUS_CSS_PATTERNS = [
    {
        "pattern": r"display\s*:\s*none\s*;",
        "issue": "Hidden elements may be used to hide malicious inputs.",
        "fix": "Ensure 'display: none' is not applied to user-controlled elements.",
        "severity": "Medium"
    },
    {
        "pattern": r"z-index\s*:\s*9999\s*;",
        "issue": "High z-index can spoof or overlay sensitive UI elements.",
        "fix": "Use conservative z-index values for layering.",
        "severity": "Low"
    },
    {
        "pattern": r"position\s*:\s*absolute\s*;.*top\s*:\s*0\s*;.*left\s*:\s*0\s*;",
        "issue": "Absolutely positioned elements at (0,0) can spoof login or UI screens.",
        "fix": "Audit positioning of full-screen UI blocks.",
        "severity": "Low"
    },
    {
        "pattern": r"pointer-events\s*:\s*none\s*;",
        "issue": "Blocks user interaction — may aid in clickjacking.",
        "fix": "Avoid pointer-events:none unless intentionally used.",
        "severity": "Low"
    },
    {
        "pattern": r"user-select\s*:\s*none\s*;",
        "issue": "Prevents text selection — may be misused to block copy/inspect.",
        "fix": "Only use user-select:none where truly needed.",
        "severity": "Low"
    }
]

def scan_files(file_list):
    findings = []

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for idx, line in enumerate(lines, start=1):
                for rule in DANGEROUS_CSS_PATTERNS:
                    if re.search(rule["pattern"], line, re.IGNORECASE):
                        findings.append({
                            "file": file_path,
                            "line": idx,
                            "code": line.strip(),
                            "issue": rule["issue"],
                            "fix": rule["fix"],
                            "severity": rule["severity"],
                            "language": "css"
                        })

        except Exception as e:
            print(f"[CSS Scanner] Error in {file_path}: {e}")

    return findings
