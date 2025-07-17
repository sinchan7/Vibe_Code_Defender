import re

def scan_file(file_path):
    jwt_tokens = []
    jwt_pattern = r'eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+'

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, start=1):
        matches = re.findall(jwt_pattern, line)
        for token in matches:
            jwt_tokens.append({
                'line': lineno,
                'token': token,
                'content': line.strip()
            })

    return jwt_tokens
