import re

DANGEROUS_CPP_PATTERNS = [
    {
        "pattern": r"\bgets\s*\(",
        "issue": "Use of gets() is unsafe and can lead to buffer overflows.",
        "fix": "Use fgets() with length limits instead.",
        "severity": "High"
    },
    {
        "pattern": r"\bstrcpy\s*\(",
        "issue": "Use of strcpy() can cause buffer overflows.",
        "fix": "Use strncpy() or safer string functions.",
        "severity": "High"
    },
    {
        "pattern": r"\bsprintf\s*\(",
        "issue": "Use of sprintf() can lead to format string vulnerabilities.",
        "fix": "Use snprintf() with length limits instead.",
        "severity": "High"
    },
    {
        "pattern": r"\bsystem\s*\(",
        "issue": "Use of system() allows command execution and may be exploited.",
        "fix": "Avoid using system(); validate input thoroughly if needed.",
        "severity": "High"
    },
    {
        "pattern": r"\bscanf\s*\(.*?%s",
        "issue": "scanf() with %s can cause buffer overflows if not limited.",
        "fix": "Use %Ns to limit input size (e.g., %32s).",
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
                for rule in DANGEROUS_CPP_PATTERNS:
                    if re.search(rule["pattern"], line):
                        findings.append({
                            "file": file_path,
                            "line": idx,
                            "code": line.strip(),
                            "issue": rule["issue"],
                            "fix": rule["fix"],
                            "severity": rule["severity"],
                            "language": "cpp"
                        })

        except Exception as e:
            print(f"[C++ Scanner] Error in {file_path}: {e}")

    return findings
