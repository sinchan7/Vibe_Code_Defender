import os
from gpt_fixer import generate_fix_with_openrouter
from patcher import apply_patch
from code_utils import extract_code_snippet

def auto_patch_all(findings):
    """
    Apply GPT-powered patches for all issues automatically.
    Returns a summary of results.
    """
    results = []

    for item in findings:
        file_path = item["file"]
        line_number = item["line"]
        issue = item["issue"]
        language = item.get("language", "python")

        # Skip if not a code-based issue
        if not file_path or not line_number or not issue:
            continue

        code_snippet = extract_code_snippet(file_path, line_number)
        if not code_snippet:
            results.append({
                "file": file_path,
                "line": line_number,
                "status": "❌ Failed to extract code",
            })
            continue

        # Generate secure fix
        suggestion = generate_fix_with_openrouter(code_snippet, issue, language)

        if suggestion.startswith("[ERROR"):
            results.append({
                "file": file_path,
                "line": line_number,
                "status": suggestion
            })
            continue

        # Apply patch
        patch_result = apply_patch(file_path, line_number, code_snippet, suggestion)
        results.append({
            "file": file_path,
            "line": line_number,
            "status": patch_result
        })

    return results
