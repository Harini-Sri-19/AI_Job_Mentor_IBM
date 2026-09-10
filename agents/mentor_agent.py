"""
AI Mentor Chat Agent.
Multi-turn conversational mentor powered by IBM Granite with RAG.
Maintains conversation history in Streamlit session state.
"""

from __future__ import annotations

from typing import Any

from rag_engine import build_rag_prompt
from watsonx_client import safe_generate

SYSTEM_PERSONA = (
    "You are Aasha, a friendly and encouraging AI Job Mentor helping informal workers in India. "
    "You provide practical, actionable guidance on jobs, skill development, government schemes, "
    "and career growth. You speak simply and clearly, avoiding jargon. "
    "You are empathetic, patient, and always supportive."
)

LANG_INSTRUCTIONS = {
    "en": "Respond in clear, simple English.",
    "hi": "हिंदी में जवाब दें। सरल और स्पष्ट भाषा का प्रयोग करें।",
    "ta": "தமிழில் பதில் அளியுங்கள். எளிமையான மொழி பயன்படுத்துங்கள்.",
}

GREETING = {
    "en": "Hello! I'm Aasha, your AI Job Mentor 🌟. I'm here to help you find better jobs, develop new skills, and access government benefits. How can I help you today?",
    "hi": "नमस्ते! मैं आशा हूँ, आपकी AI जॉब मेंटर 🌟। मैं आपको बेहतर नौकरी खोजने, नए कौशल विकसित करने और सरकारी लाभ प्राप्त करने में मदद करने के लिए यहाँ हूँ। आज मैं आपकी कैसे मदद कर सकती हूँ?",
    "ta": "வணக்கம்! நான் ஆஷா, உங்கள் AI வேலை வழிகாட்டி 🌟। நான் உங்களுக்கு சிறந்த வேலைகள் கண்டுபிடிக்க, புதிய திறன்கள் வளர்க்க, மற்றும் அரசு நலத்திட்டங்களை பெற உதவுவேன். இன்று நான் உங்களுக்கு எவ்வாறு உதவலாம்?",
}


def build_chat_prompt(
    user_message: str,
    history: list[dict[str, str]],
    worker: dict[str, Any] | None,
    language: str,
) -> str:
    """Build a multi-turn prompt with conversation history and worker context."""
    lang_inst = LANG_INSTRUCTIONS.get(language, LANG_INSTRUCTIONS["en"])

    # Worker context block
    worker_ctx = ""
    if worker:
        worker_ctx = (
            f"Worker context:\n"
            f"- Name: {worker.get('name')}, Age: {worker.get('age')}, Location: {worker.get('location')}\n"
            f"- Job: {worker.get('current_occupation')}, Income: ₹{worker.get('monthly_income')}/month\n"
            f"- Skills: {', '.join(worker.get('skills', []))}\n"
            f"- Education: {worker.get('education')}\n\n"
        )

    # Build conversation history string (last 6 turns max)
    history_str = ""
    for turn in history[-6:]:
        role = "Worker" if turn["role"] == "user" else "Aasha"
        history_str += f"{role}: {turn['content']}\n"

    prompt = (
        f"{SYSTEM_PERSONA}\n"
        f"{lang_inst}\n\n"
        f"{worker_ctx}"
        f"Conversation so far:\n{history_str}"
        f"Worker: {user_message}\n"
        f"Aasha:"
    )
    return prompt


def get_mentor_response(
    user_message: str,
    history: list[dict[str, str]],
    worker: dict[str, Any] | None = None,
    language: str = "en",
) -> tuple[str, bool]:
    """
    Generate a mentor response for the given user message.
    Returns (response_text, is_live_ai).
    """
    base_prompt = build_chat_prompt(user_message, history, worker, language)
    rag_prompt = build_rag_prompt(base_prompt, user_message, top_k=2)
    return safe_generate(rag_prompt, fallback_key="chat", max_tokens=400)


def get_greeting(language: str = "en") -> str:
    return GREETING.get(language, GREETING["en"])
