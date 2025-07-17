import re

# Basic patterns for common dangerous function names across languages
UNSAFE_FUNCTIONS = [
    'eval', 'exec', 'system', 'popen', 'ProcessBuilder', 'Runtime\.getRuntime\(\)', 
    'shell_exec', 'os.system', 'subprocess.call', 'child_process.exec',
    'document.write', 'innerHTML\s*=', 'setTimeout\\(', 'setInterval\\('
]

def scan_file(file_path):
    issues = []
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    for lineno, line in enumerate(lines, start=1):
        for func in UNSAFE_FUNCTIONS:
            if re.search(rf'\b{func}\b', line):
                issues.append({
                    'function': func,
                    'line': lineno,
                    'content': line.strip()
                })

    return issues
