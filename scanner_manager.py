from detectors.language_detector import detect_languages
from scanners.python import secrets, unsafe_calls, jwt_check
from scanners.javascript.eslint_scanner import scan_files as scan_js
from scanners.java.java_scanner import scan_files as scan_java
from scanners.cpp.cpp_scanner import scan_files as scan_cpp
from scanners.html.html_scanner import scan_files as scan_html
from scanners.css.css_scanner import scan_files as scan_css
from scanners.multi.semgrep_scanner import scan_files as scan_semgrep

def scan_project(project_path, use_semgrep=False):
    all_findings = []

    # Detect files by language
    language_map = detect_languages(project_path)

    # Route to each language-specific scanner
    for lang, files in language_map.items():
        if lang == "python":
            for file in files:
                all_findings += secrets.scan_file(file)
                all_findings += unsafe_calls.scan_file(file)
                all_findings += jwt_check.scan_file(file)

        elif lang == "javascript":
            all_findings += scan_js(files)

        elif lang == "java":
            all_findings += scan_java(files)

        elif lang == "cpp":
            all_findings += scan_cpp(files)

        elif lang == "html":
            all_findings += scan_html(files)

        elif lang == "css":
            all_findings += scan_css(files)

    # Optional: run semgrep on all files (multi-language coverage)
    if use_semgrep:
        all_code_files = [f for flist in language_map.values() for f in flist]
        all_findings += scan_semgrep(all_code_files)

    return all_findings


# Optional CLI test
if __name__ == "__main__":
    from pprint import pprint
    results = scan_project("uploaded_project", use_semgrep=True)
    pprint(results)
