"""
IBM watsonx.ai client using IBM Granite model.
Falls back to rule-based responses if API is unavailable.
"""

import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

WATSONX_API_KEY    = os.getenv("WATSONX_API_KEY", "")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID", "ce28f6ea-0113-4fea-b875-01da6c4b5897")
WATSONX_MODEL_ID   = os.getenv("WATSONX_MODEL_ID",   "ibm/granite-4-h-small")
# Always target the chat endpoint (granite-4-h-small is a chat/instruct model)
_CHAT_URL = (
    "https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29"
)
IAM_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"

_iam_token_cache: dict = {"token": None, "expires_at": 0}


def _get_iam_token() -> str:
    """Fetch IAM bearer token from IBM Cloud, with simple in-memory cache."""
    if _iam_token_cache["token"] and time.time() < _iam_token_cache["expires_at"] - 60:
        return _iam_token_cache["token"]

    resp = requests.post(
        IAM_TOKEN_URL,
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": WATSONX_API_KEY,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    _iam_token_cache["token"] = data["access_token"]
    _iam_token_cache["expires_at"] = time.time() + int(data.get("expires_in", 3600))
    return _iam_token_cache["token"]


def _prompt_to_messages(prompt: str) -> tuple[str, str]:
    """
    Split a composite prompt string into (system_text, user_text).

    The agents build prompts that begin with persona/instruction lines and end
    with the actual content to generate.  We separate at the first blank line
    that follows instruction-style sentences so Granite receives a proper
    system+user message pair.
    """
    lines = prompt.split("\n")
    # Collect leading instruction/persona lines as the system message.
    # Stop when we hit the first substantive content block (contains "Worker:",
    # "Conversation", "Use the following", or a long paragraph).
    system_lines: list[str] = []
    user_lines: list[str] = []
    in_user = False
    for line in lines:
        if not in_user:
            stripped = line.strip()
            # Transition triggers: RAG context block, worker context, conversation
            if (
                stripped.startswith("Use the following")
                or stripped.startswith("Worker context")
                or stripped.startswith("Conversation so far")
                or stripped.startswith("Worker profile")
                or stripped.startswith("Worker:")
                or stripped.startswith("Job: ")
                or stripped.startswith("[JOB")
                or stripped.startswith("[TRAINING")
                or stripped.startswith("[SCHEME")
                or stripped.startswith("[SKILL")
            ):
                in_user = True
                user_lines.append(line)
            else:
                system_lines.append(line)
        else:
            user_lines.append(line)

    system_text = "\n".join(system_lines).strip()
    user_text   = "\n".join(user_lines).strip()

    # If we couldn't split (no trigger found), treat whole prompt as user message
    if not user_text:
        return "", prompt.strip()

    return system_text, user_text


def generate_text(prompt: str, max_tokens: int = 512, temperature: float = 0.7) -> str:
    """
    Call IBM Granite via the watsonx.ai text/chat endpoint.
    Accepts the same prompt string interface used by all agents, converts it
    internally to the messages format required by granite-4-h-small.
    Returns generated text string, or raises on failure.
    """
    token = _get_iam_token()

    system_text, user_text = _prompt_to_messages(prompt)

    messages = []
    if system_text:
        messages.append({"role": "system", "content": system_text})
    messages.append({"role": "user", "content": user_text})

    payload = {
        "model_id": WATSONX_MODEL_ID,
        "project_id": WATSONX_PROJECT_ID,
        "messages": messages,
        "parameters": {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "repetition_penalty": 1.1,
        },
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    resp = requests.post(_CHAT_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    return result["choices"][0]["message"]["content"].strip()


# ---------------------------------------------------------------------------
# Fallback responses when API is unavailable
# ---------------------------------------------------------------------------

FALLBACK_RESPONSES = {
    "job_recommendation": (
        "Based on your profile, here are suitable job options:\n"
        "1. **Construction Supervisor** – Your experience in manual labour and team coordination aligns well.\n"
        "2. **Delivery Associate** – Flexible hours, basic smartphone literacy required.\n"
        "3. **Domestic Electrician Helper** – Short training can upgrade your earning potential."
    ),
    "skill_gap": (
        "Here are some key areas to focus on for your target role:\n"
        "• **Digital literacy** – Basic smartphone and app usage\n"
        "• **Financial management** – Budgeting and savings\n"
        "• **Communication** – Workplace Hindi/English basics"
    ),
    "training": (
        "Recommended training programmes to get you started:\n"
        "1. **PMKVY Skill Course** – Free government-certified training\n"
        "2. **Digital Saksharta Abhiyan** – Digital literacy (online)\n"
        "3. **ITI Certificate Course** – 6-month vocational training"
    ),
    "scheme": (
        "Government schemes you may be eligible for:\n"
        "1. **PM-SYM** – Pension scheme for informal workers\n"
        "2. **ESIC** – Health insurance\n"
        "3. **PMJDY** – Zero-balance bank account"
    ),
    "chat": (
        "Sorry, I'm temporarily unable to respond. Please try again in a moment."
    ),
}


def safe_generate(prompt: str, fallback_key: str = "chat", max_tokens: int = 512) -> tuple[str, bool]:
    """
    Try watsonx.ai; return (text, is_live).
    Falls back gracefully with a pre-defined response.
    """
    if not WATSONX_API_KEY:
        return FALLBACK_RESPONSES.get(fallback_key, FALLBACK_RESPONSES["chat"]), False
    try:
        text = generate_text(prompt, max_tokens=max_tokens)
        return text, True
    except Exception:
        return FALLBACK_RESPONSES.get(fallback_key, FALLBACK_RESPONSES["chat"]), False
