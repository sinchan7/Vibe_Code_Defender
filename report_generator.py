from collections import defaultdict

def generate_report(findings):
    if not findings:
        return "# ✅ Defender Scan Report\n\nNo major issues found.\n"

    report = "# 🛡️ Defender App Scan Report\n\n"

    # Group by language
    lang_group = defaultdict(list)
    for item in findings:
        lang_group[item['language']].append(item)

    for lang, items in lang_group.items():
        report += f"## 🔍 {lang.upper()} Findings\n\n"
        for item in items:
            report += f"**File:** `{item['file']}`  \n"
            report += f"**Line:** {item['line']}  \n"
            report += f"**Severity:** `{item['severity']}`  \n"
            report += f"**Issue:** {item['issue']}  \n"
            report += f"**Code:** `{item['code']}`  \n"
            report += f"**Fix:** {item['fix']}  \n\n"
        report += "---\n\n"

    return report
