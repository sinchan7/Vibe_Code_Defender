import subprocess
import json
import os

def scan_files(file_list):
    findings = []

    for file_path in file_list:
        try:
            result = subprocess.run(
                ["semgrep", "--quiet", "--json", file_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0 or not result.stdout.strip():
                continue  # No findings

            semgrep_output = json.loads(result.stdout)

            for finding in semgrep_output.get("results", []):
                findings.append({
                    "file": finding["path"],
                    "line": finding["start"]["line"],
                    "code": finding.get("extra", {}).get("code", "").strip(),
                    "issue": finding.get("check_id", "Semgrep finding"),
                    "fix": finding.get("extra", {}).get("message", "Review this pattern."),
                    "severity": finding.get("extra", {}).get("severity", "Medium").capitalize(),
                    "language": os.path.splitext(file_path)[1].lstrip(".").lower()
                })

        except Exception as e:
            print(f"[Semgrep Scanner] Failed on {file_path}: {e}")

    return findings
