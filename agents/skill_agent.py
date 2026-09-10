"""
Skill Gap Analysis Agent.
Identifies skill gaps between a worker's current skills and
target job requirements. Uses IBM Granite for detailed analysis.
"""

from __future__ import annotations

from typing import Any

from data.demo_data import SKILL_TAXONOMY, JOB_SKILL_REQUIREMENTS
from rag_engine import build_rag_prompt
from watsonx_client import safe_generate


def _normalise(skill: str) -> str:
    return skill.lower().strip()


def get_skill_gaps(worker_skills: list[str], target_job: str) -> dict[str, Any]:
    """
    Compare worker skills against target job requirements.
    Returns present skills, missing skills, and gap severity.
    """
    req_map = JOB_SKILL_REQUIREMENTS.get(target_job, {})
    required_flat: list[str] = []
    for skills in req_map.values():
        required_flat.extend(skills)

    worker_norm = {_normalise(s) for s in worker_skills}

    present, missing = [], []
    for skill in required_flat:
        sn = _normalise(skill)
        matched = any(sn in wn or wn in sn for wn in worker_norm)
        if matched:
            present.append(skill)
        else:
            missing.append(skill)

    # Also infer gaps by taxonomy category
    category_gaps: dict[str, list[str]] = {}
    for category, tax_skills in SKILL_TAXONOMY.items():
        for ts in tax_skills:
            if _normalise(ts) not in worker_norm:
                category_gaps.setdefault(category, []).append(ts)

    gap_percent = (len(missing) / max(len(required_flat), 1)) * 100

    return {
        "target_job": target_job,
        "total_required": len(required_flat),
        "present_skills": present,
        "missing_skills": missing,
        "gap_percentage": round(gap_percent),
        "readiness_percentage": round(100 - gap_percent),
        "category_gaps": category_gaps,
    }


def get_all_skill_gaps(worker: dict[str, Any]) -> list[dict[str, Any]]:
    """Compute skill gaps for all defined target jobs."""
    results = []
    for job in JOB_SKILL_REQUIREMENTS:
        gap = get_skill_gaps(worker.get("skills", []), job)
        results.append(gap)
    results.sort(key=lambda x: x["readiness_percentage"], reverse=True)
    return results


def get_skill_gap_narrative(
    worker: dict[str, Any],
    gap_analysis: dict[str, Any],
    language: str = "en",
) -> tuple[str, bool]:
    """Use IBM Granite to generate a motivating skill gap analysis narrative."""
    lang_inst = {
        "ta": "Respond in Tamil language.",
        "hi": "Respond in Hindi language.",
        "en": "Respond in English.",
    }.get(language, "Respond in English.")

    query = f"skill gap analysis {gap_analysis.get('target_job', '')} {' '.join(gap_analysis.get('missing_skills', []))}"

    base_prompt = (
        f"{lang_inst}\n\n"
        f"You are a career counsellor helping an informal worker in India.\n"
        f"Worker: {worker.get('name')}, Current skills: {', '.join(worker.get('skills', []))}\n"
        f"Target job: {gap_analysis.get('target_job')}\n"
        f"Job readiness: {gap_analysis.get('readiness_percentage')}%\n"
        f"Skills already present: {', '.join(gap_analysis.get('present_skills', [])) or 'None'}\n"
        f"Missing skills: {', '.join(gap_analysis.get('missing_skills', [])) or 'None'}\n\n"
        f"Write a short (3–4 sentences) encouraging analysis. Acknowledge what they already know, "
        f"and explain clearly which 1–2 skills are most important to acquire next and why."
    )

    prompt = build_rag_prompt(base_prompt, query, doc_type="skill")
    return safe_generate(prompt, fallback_key="skill_gap", max_tokens=300)
