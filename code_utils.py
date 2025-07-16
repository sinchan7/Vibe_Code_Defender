import os

def extract_code_snippet(file_path, line_number, context_lines=3):
    """
    Extracts a code snippet from any file with ± context_lines around the target line number.
    Works with all languages (Python, JS, Java, C++, HTML, etc).
    """

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        total_lines = len(lines)
        start = max(0, line_number - context_lines - 1)
        end = min(total_lines, line_number + context_lines)

        snippet = ''.join(lines[start:end])
        return snippet.strip()

    except Exception as e:
        return f"# Failed to extract code snippet from {file_path}: {e}"
