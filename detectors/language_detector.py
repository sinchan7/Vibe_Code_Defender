import os
from collections import defaultdict

EXTENSION_TO_LANG = {
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
}

def detect_languages(project_path):
    language_files = defaultdict(list)

    for root, _, files in os.walk(project_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            language = EXTENSION_TO_LANG.get(ext)
            if language:
                full_path = os.path.join(root, file)
                language_files[language].append(full_path)

    return dict(language_files)

# Example test
if __name__ == "__main__":
    result = detect_languages("uploaded_project")
    for lang, files in result.items():
        print(f"{lang.upper()} ({len(files)} files):")
        for f in files:
            print(" -", f)
