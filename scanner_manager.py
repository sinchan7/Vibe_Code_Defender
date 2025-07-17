import os
import importlib

# Maps file extensions to language names
EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".cc": "cpp",
    ".html": "html",
    ".htm": "html",
    ".css": "css"
}

SCANNER_TYPES = ["secrets", "unsafe_calls", "jwt"]

def dynamic_import(lang, scanner_type):
    """Dynamically import a scanner module for a given language and type."""
    try:
        return importlib.import_module(f"scanners.{lang}.{scanner_type}_scanner")
    except ModuleNotFoundError:
        return None

def scan_project(project_path, selected_languages=None):
    secrets_results = []
    unsafe_results = []
    jwt_results = []

    for root, _, files in os.walk(project_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            _, ext = os.path.splitext(filename.lower())

            lang = EXTENSION_MAP.get(ext)
            if not lang:
                continue

            # 🟨 Only scan if selected
            if selected_languages and lang not in selected_languages:
                continue

            print(f"[SCAN] Scanning {file_path} as {lang}")

            try:
                # === Run secrets scanner ===
                if (secrets_mod := dynamic_import(lang, "secrets")):
                    secrets_results += secrets_mod.scan_file(file_path)

                # === Run unsafe calls scanner ===
                if (unsafe_mod := dynamic_import(lang, "unsafe_calls")):
                    unsafe_results += unsafe_mod.scan_file(file_path)

                # === Run JWT scanner ===
                if (jwt_mod := dynamic_import(lang, "jwt")):
                    jwt_results += jwt_mod.scan_file(file_path)

            except Exception as e:
                print(f"[ERROR] Scanning {file_path} failed: {str(e)}")

    return secrets_results, unsafe_results, jwt_results
