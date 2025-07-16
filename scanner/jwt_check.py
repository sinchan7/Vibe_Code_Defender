import os
import re

def scan_jwt(base_path):
    results = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") or file.endswith(".json"):
                path = os.path.join(root, file)
                with open(path, "r", errors="ignore") as f:
                    content = f.read()
                    if '"alg": "none"' in content:
                        results.append({
                            "file": path,
                            "line": "N/A",
                            "issue": "JWT uses insecure algorithm: 'none'",
                            "fix": "Use HS256 or RS256 and validate signatures server-side."
                        })
                    if '"alg":' in content and '"exp":' not in content:
                        results.append({
                            "file": path,
                            "line": "N/A",
                            "issue": "JWT has no expiration (`exp`)",
                            "fix": "Always include `exp` claim in JWTs to avoid indefinite validity."
                        })
    return results
