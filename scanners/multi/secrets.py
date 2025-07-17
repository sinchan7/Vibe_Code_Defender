import re

def scan_file(file_path):
    secrets_found = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    secret_patterns = {
        'AWS Access Key': r'AKIA[0-9A-Z]{16}',
        'AWS Secret Key': r'(?<![A-Z0-9])[A-Za-z0-9/+=]{40}(?![A-Z0-9])',
        'Generic API Key': r'(?i)(api[_-]?key|secret)[\'"\s:=]{1,}[0-9a-zA-Z]{16,45}',
        'Private Key Block': r'-----BEGIN(.*?)PRIVATE KEY-----'
    }

    for lineno, line in enumerate(lines, start=1):
        for name, pattern in secret_patterns.items():
            if re.search(pattern, line):
                secrets_found.append({
                    'type': name,
                    'line': lineno,
                    'content': line.strip()
                })

    return secrets_found
