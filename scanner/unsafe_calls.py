import os
import ast

DANGEROUS_FUNCS = {
    "eval": "Avoid using `eval()`; use safe parsing or `ast.literal_eval()` if needed.",
    "exec": "Avoid `exec()`; refactor logic to avoid dynamic execution.",
    "system": "Avoid `os.system()`; use `subprocess.run()` with proper input handling.",
}

def scan_unsafe_calls(base_path):
    results = []
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", errors="ignore") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                    except:
                        continue

                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            if hasattr(node.func, 'id') and node.func.id in DANGEROUS_FUNCS:
                                results.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "issue": f"Use of `{node.func.id}()`",
                                    "code": "",  # Optional: read line
                                    "fix": DANGEROUS_FUNCS[node.func.id]
                                })
                            elif hasattr(node.func, 'attr') and node.func.attr == "system":
                                results.append({
                                    "file": file_path,
                                    "line": node.lineno,
                                    "issue": "Use of `os.system()`",
                                    "code": "",
                                    "fix": DANGEROUS_FUNCS["system"]
                                })
    return results
