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
    Replace code at a given line number (± context) with the new AI-generated code.
    """

    ensure_backup(file_path)

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        # Determine the best line to replace (exact match or surrounding)
        patch_block_start = max(0, line_number - 3)
        patch_block_end = min(len(lines), line_number + 2)

        # Replace block with GPT output (split into lines)
        new_code_lines = new_code.strip().splitlines(keepends=False)
        new_code_lines = [line + '\n' for line in new_code_lines]

        updated_lines = (
            lines[:patch_block_start] +
            new_code_lines +
            lines[patch_block_end:]
        )

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)

        return f"✅ Patch applied to {file_path} (original backed up in /{BACKUP_DIR})"

    except Exception as e:
        return f"❌ Failed to apply patch: {str(e)}"
