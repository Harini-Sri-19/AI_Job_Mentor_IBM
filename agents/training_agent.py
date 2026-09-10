"""
Training Recommendation Agent.
Matches worker skill gaps with relevant training programmes.
Uses IBM Granite for personalised training path narratives.
"""

from __future__ import annotations

from typing import Any

from data.demo_data import TRAINING_PROGRAMMES
from rag_engine import build_rag_prompt
from watsonx_client import safe_generate


def _skill_overlap(needed_skills: list[str], programme_skills: list[str]) -> float:
    if not needed_skills:
        return 0.0
    needed_lower = {s.lower() for s in needed_skills}
    prog_lower = {s.lower() for s in programme_skills}
    overlap = sum(
        1 for ns in needed_lower
        if any(ns in ps or ps in ns for ps in prog_lower)
    )
    return overlap / len(needed_skills)


def get_training_recommendations(
    worker: dict[str, Any],
    missing_skills: list[str],
    top_n: int = 4,
) -> list[dict[str, Any]]:
    """
    Recommend training programmes that address the worker's skill gaps.
    Returns programmes sorted by relevance score.
    """
    results = []
    for prog in TRAINING_PROGRAMMES:
        # Skill relevance
        skill_rel = _skill_overlap(missing_skills, prog["skills_covered"])

        # Cost score (free = 1.0, paid = lower)
        cost_score = 1.0 if prog["cost"].lower() == "free" else 0.7 if "subsidis" in prog["cost"].lower() else 0.5

        # Language match
        worker_langs = {l.lower() for l in worker.get("languages", ["Hindi"])}
        prog_langs = {l.lower() for l in prog.get("languages", [])}
        lang_score = 1.0 if worker_langs & prog_langs else 0.6

        # Mode score: prefer online for workers without easy access
        mode_score = 0.9 if "online" in prog.get("mode", "").lower() else 1.0

        relevance = round((skill_rel * 0.5 + cost_score * 0.25 + lang_score * 0.15 + mode_score * 0.10) * 100)
        results.append({**prog, "relevance_score": relevance})

    results.sort(key=lambda x: x["relevance_score"], reverse=True)
    return results[:top_n]


def get_training_narrative(
    worker: dict[str, Any],
    recommended: list[dict[str, Any]],
    missing_skills: list[str],
    language: str = "en",
) -> tuple[str, bool]:
    """Generate a personalised training path narrative using IBM Granite."""
    lang_inst = {
        "ta": "Respond in Tamil language.",
        "hi": "Respond in Hindi language.",
        "en": "Respond in English.",
    }.get(language, "Respond in English.")

    prog_summaries = "\n".join(
        f"- {p['name']} ({p['duration']}, {p['cost']}): covers {', '.join(p['skills_covered'][:3])}"
        for p in recommended[:3]
    )

    query = f"training programmes skill development {' '.join(missing_skills[:5])}"

    base_prompt = (
        f"{lang_inst}\n\n"
        f"You are a career development adviser for informal workers in India.\n"
        f"Worker: {worker.get('name')}, Education: {worker.get('education')}\n"
        f"Skills to develop: {', '.join(missing_skills) or 'General upskilling'}\n\n"
        f"Recommended training:\n{prog_summaries}\n\n"
        f"Write 3–4 sentences: which programme to start first, why it matters for their career, "
        f"and one practical tip for completing it successfully."
    )

    prompt = build_rag_prompt(base_prompt, query, doc_type="training")
    return safe_generate(prompt, fallback_key="training", max_tokens=300)
