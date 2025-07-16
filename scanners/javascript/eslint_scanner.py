import re

DANGEROUS_PATTERNS = [
    {
        "pattern": r"\beval\s*\(",
        "issue": "Use of eval() is dangerous and can lead to code injection.",
        "fix": "Avoid using eval(); use JSON.parse or other safer methods.",
        "severity": "High"
    },
    {
        "pattern": r"document\.write\s*\(",
        "issue": "document.write() can lead to XSS vulnerabilities.",
        "fix": "Avoid document.write(); use DOM methods like createElement().",
        "severity": "High"
    },
    {
        "pattern": r"\.innerHTML\s*=",
        "issue": "Assigning to innerHTML can open the door to XSS.",
        "fix": "Use textContent or proper sanitization libraries.",
        "severity": "High"
    },
    {
        "pattern": r"\bnew\s+Function\s*\(",
        "issue": "Dynamic function creation is equivalent to eval().",
        "fix": "Avoid new Function(); use static functions.",
        "severity": "High"
    },
    {
        "pattern": r"localStorage\s*\.\s*setItem\s*\(",
        "issue": "Storing sensitive data in localStorage can expose it to XSS.",
        "fix": "Avoid storing tokens in localStorage; use httpOnly cookies.",
        "severity": "Medium"
    }
]

def scan_files(file_list):
    findings = []

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for idx, line in enumerate(lines, start=1):
                for rule in DANGEROUS_PATTERNS:
                    if re.search(rule["pattern"], line):
                        findings.append({
                            "file": file_path,
                            "line": idx,
                            "code": line.strip(),
                            "issue": rule["issue"],
                            "fix": rule["fix"],
                            "severity": rule["severity"],
                            "language": "javascript"
                        })

        except Exception as e:
            print(f"[JS Scanner] Error reading {file_path}: {e}")

    return findings
