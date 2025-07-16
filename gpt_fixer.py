import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_fix_with_openrouter(code_snippet, issue_description, language="python"):
    prompt = f"""
The following {language} code has a security issue:
{issue_description}

Please rewrite it securely and explain the changes.
Only output the rewritten code, no explanations.

Code:
{code_snippet}
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://defender-app.local",  # Optional
        "Content-Type": "application/json"
    }

    data = {
        "model": "deepseek/deepseek-chat-v3-0324",  # You can change this model
        "messages": [
            {
                "role": "system",
                "content": f"You are a secure coding assistant that fixes vulnerabilities in {language}."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"[ERROR {response.status_code}] {response.text}"
    except Exception as e:
        return f"[ERROR] {str(e)}"
