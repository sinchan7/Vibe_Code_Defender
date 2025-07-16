import os
import shutil

BACKUP_DIR = "backup"

def ensure_backup(file_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
    
    # Only backup once per session
    if not os.path.exists(backup_path):
        shutil.copy(file_path, backup_path)

def apply_patch(file_path, line_number, original_code, new_code):
    """
    Replace the original line with new secure code at the given line_number.
    Works across any language (Python, JS, C++, etc).
    """

    ensure_backup(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        original_line = lines[line_number - 1].strip()
        if original_code.strip() not in original_line:
            return f"⚠️ Original code mismatch at {file_path}:{line_number}. Patch skipped."

        # Respect existing indentation
        indent = len(lines[line_number - 1]) - len(lines[line_number - 1].lstrip())
        indent_spaces = " " * indent

        # Insert new code with matching indent
        new_code_lines = new_code.strip().splitlines()
        indented_lines = [(indent_spaces + line).rstrip() + '\n' for line in new_code_lines]

        lines[line_number - 1] = "".join(indented_lines)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        return f"✅ Patch applied to {file_path}:{line_number} (original backed up in /{BACKUP_DIR})"

    except Exception as e:
        return f"❌ Failed to apply patch: {str(e)}"
