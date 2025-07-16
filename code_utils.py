import os

def extract_code_snippet(file_path, line_number, context_lines=3):
    try:
        with open(file_path, 'r', errors='ignore') as f:
            lines = f.readlines()

        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        snippet = ''.join(lines[start:end])

        return snippet.strip()
    except:
        return ""
