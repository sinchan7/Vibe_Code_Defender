
import streamlit as st
import zipfile
import os
import io
import shutil
from scanner.secrets import scan_secrets
from scanner.unsafe_calls import scan_unsafe_calls
from scanner.jwt_check import scan_jwt
from gpt_fixer import generate_fix_with_openrouter
from code_utils import extract_code_snippet
from patcher import apply_patch

st.set_page_config(page_title="Defender App", layout="wide")
st.title("🛡️ Defender App - Secure Your Vibe Code")

uploaded_file = st.file_uploader("Upload your project ZIP file", type=["zip"])

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        extract_path = "uploaded_project"
        if os.path.exists(extract_path):
            shutil.rmtree(extract_path)
        zip_ref.extractall(extract_path)

    st.success("✅ Project extracted. Scanning...")

    # Run all scanners
    secret_results = scan_secrets(extract_path)
    unsafe_results = scan_unsafe_calls(extract_path)
    jwt_results = scan_jwt(extract_path)

    st.subheader("🔐 Hardcoded Secrets")
    for item in secret_results:
        with st.expander(f"{item['file']} : Line {item['line']}"):
            st.code(item['code'])
            st.error(item['issue'])
            st.info(item['fix'])

    st.subheader("⚠️ Unsafe Function Calls")
    for item in unsafe_results:
        with st.expander(f"{item['file']} : Line {item['line']}"):
            code_snippet = extract_code_snippet(item['file'], item['line'])
            st.code(code_snippet, language="python")
            st.error(item['issue'])
            st.info(item['fix'])

            if st.button(f"🔮 Generate Fix with AI ({item['file']}:{item['line']})", key=f"fix_{item['file']}_{item['line']}"):
                with st.spinner("Asking AI..."):
                    suggestion = generate_fix_with_openrouter(code_snippet, item['issue'])
                    st.success("Here is the suggested secure fix:")
                    st.code(suggestion, language="python")

                    if st.button(f"💾 Apply Fix to {item['file']}:{item['line']}", key=f"patch_{item['file']}_{item['line']}"):
                        result = apply_patch(item['file'], item['line'], code_snippet, suggestion)
                        st.success(result)

    st.subheader("🔓 JWT Issues")
    for item in jwt_results:
        with st.expander(f"{item['file']}"):
            st.error(item['issue'])
            st.info(item['fix'])

    # Combine all results into one string
    def generate_report_text(secret_results, unsafe_results, jwt_results):
        report = "# 🛡️ Defender App Scan Report\n\n"

        if secret_results:
            report += "## 🔐 Hardcoded Secrets\n"
            for item in secret_results:
                report += f"- **{item['file']} : Line {item['line']}**\n"
                report += f"  - Issue: {item['issue']}\n"
                report += f"  - Code: `{item['code']}`\n"
                report += f"  - Fix: {item['fix']}\n\n"

        if unsafe_results:
            report += "## ⚠️ Unsafe Function Calls\n"
            for item in unsafe_results:
                report += f"- **{item['file']} : Line {item['line']}**\n"
                report += f"  - Issue: {item['issue']}\n"
                report += f"  - Fix: {item['fix']}\n\n"

        if jwt_results:
            report += "## 🔓 JWT Issues\n"
            for item in jwt_results:
                report += f"- **{item['file']}**\n"
                report += f"  - Issue: {item['issue']}\n"
                report += f"  - Fix: {item['fix']}\n\n"

        if not any([secret_results, unsafe_results, jwt_results]):
            report += "✅ No major issues found.\n"

        return report

    # Generate and show download button
    report_content = generate_report_text(secret_results, unsafe_results, jwt_results)
    report_bytes = io.BytesIO(report_content.encode("utf-8"))

    st.download_button(
        label="📥 Download Full Report",
        data=report_bytes,
        file_name="defender_report.md",
        mime="text/markdown"
    )
