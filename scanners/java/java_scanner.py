import re

DANGEROUS_JAVA_PATTERNS = [
    {
        "pattern": r"Runtime\.getRuntime\(\)\.exec\(",
        "issue": "Potential command injection via Runtime.exec().",
        "fix": "Use ProcessBuilder with validated arguments.",
        "severity": "High"
    },
    {
        "pattern": r"(SELECT|INSERT|UPDATE|DELETE)\s+.*?FROM",
        "issue": "Potential raw SQL string — vulnerable to SQL injection.",
        "fix": "Use prepared statements (e.g., PreparedStatement).",
        "severity": "High"
    },
    {
        "pattern": r"password\s*=\s*['\"].+?['\"]",
        "issue": "Hardcoded password detected.",
        "fix": "Use environment variables or secure config files.",
        "severity": "High"
    },
    {
        "pattern": r"System\.out\.println\(.{0,50}password.{0,50}\)",
        "issue": "Possible logging of sensitive credentials.",
        "fix": "Never log passwords or secrets.",
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
                for rule in DANGEROUS_JAVA_PATTERNS:
                    if re.search(rule["pattern"], line, re.IGNORECASE):
                        findings.append({
                            "file": file_path,
                            "line": idx,
                            "code": line.strip(),
                            "issue": rule["issue"],
                            "fix": rule["fix"],
                            "severity": rule["severity"],
                            "language": "java"
                        })

        except Exception as e:
            print(f"[Java Scanner] Error in {file_path}: {e}")

    return findings
