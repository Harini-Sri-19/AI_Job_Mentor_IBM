"""
Job Recommendation Agent.
Computes match scores between a worker profile and available job listings.
Uses IBM Granite (via RAG) for narrative recommendations.
"""

from __future__ import annotations

from typing import Any

from data.demo_data import JOB_LISTINGS
from rag_engine import build_rag_prompt
from watsonx_client import safe_generate


def _skill_overlap_score(worker_skills: list[str], required_skills: list[str]) -> float:
    """Return fraction of required skills the worker already has (case-insensitive partial match)."""
    if not required_skills:
        return 1.0
    worker_lower = {s.lower() for s in worker_skills}
    matched = 0
    for rs in required_skills:
        rs_lower = rs.lower()
        if any(rs_lower in ws or ws in rs_lower for ws in worker_lower):
            matched += 1
    return matched / len(required_skills)


def _education_score(worker_edu: str, required_edu: str) -> float:
    order = [
        "no minimum", "class 5", "class 8", "class 10", "ssc",
        "class 12", "hsc", "iti", "iti certificate", "diploma",
        "graduate", "post graduate",
    ]
    w = next((i for i, e in enumerate(order) if e in worker_edu.lower()), 0)
    r = next((i for i, e in enumerate(order) if e in required_edu.lower()), 0)
    return 1.0 if w >= r else max(0.0, 1.0 - (r - w) * 0.2)


def _experience_score(worker_exp: int, required_exp: int) -> float:
    if required_exp == 0:
        return 1.0
    return min(1.0, worker_exp / required_exp)


def compute_match_score(worker: dict[str, Any], job: dict[str, Any]) -> dict[str, Any]:
    """Return a dict with overall match score (0–100) and component breakdown."""
    skill_sc = _skill_overlap_score(worker.get("skills", []), job.get("required_skills", []))
    edu_sc = _education_score(worker.get("education", ""), job.get("required_education", "No minimum"))
    exp_sc = _experience_score(worker.get("experience_years", 0), job.get("experience_required", 0))

    # Salary fit: does upper salary bracket match worker's growth expectation?
    income_ratio = min(1.0, job.get("salary_max", 0) / max(worker.get("monthly_income", 1) * 1.2, 1))
    income_sc = min(1.0, income_ratio)

    overall = round((skill_sc * 0.45 + edu_sc * 0.20 + exp_sc * 0.25 + income_sc * 0.10) * 100)

    return {
        "overall": overall,
        "skill_match": round(skill_sc * 100),
        "education_fit": round(edu_sc * 100),
        "experience_fit": round(exp_sc * 100),
        "salary_potential": round(income_sc * 100),
    }


def get_job_recommendations(worker: dict[str, Any], top_n: int = 5) -> list[dict[str, Any]]:
    """Return top job matches for a worker, sorted by match score."""
    results = []
    for job in JOB_LISTINGS:
        scores = compute_match_score(worker, job)
        results.append({**job, "match": scores})
    results.sort(key=lambda x: x["match"]["overall"], reverse=True)
    return results[:top_n]


def get_recommendation_narrative(worker: dict[str, Any], top_jobs: list[dict[str, Any]], language: str = "en") -> tuple[str, bool]:
    """Use IBM Granite (RAG) to generate a personalised recommendation narrative."""
    lang_inst = {
        "ta": "Respond in Tamil language.",
        "hi": "Respond in Hindi language.",
        "en": "Respond in English.",
    }.get(language, "Respond in English.")

    job_summaries = "\n".join(
        f"- {j['title']} (Match: {j['match']['overall']}%): {j['description']}"
        for j in top_jobs[:3]
    )

    query = f"{worker.get('current_occupation', '')} job recommendations skills {' '.join(worker.get('skills', []))}"

    base_prompt = (
        f"{lang_inst}\n\n"
        f"You are an AI Job Mentor helping an informal worker in India.\n"
        f"Worker profile:\n"
        f"- Name: {worker.get('name')}, Age: {worker.get('age')}, Location: {worker.get('location')}\n"
        f"- Current job: {worker.get('current_occupation')}, Income: ₹{worker.get('monthly_income')}/month\n"
        f"- Skills: {', '.join(worker.get('skills', []))}\n"
        f"- Education: {worker.get('education')}\n\n"
        f"Top matching jobs:\n{job_summaries}\n\n"
        f"Write a brief (3–4 sentences), encouraging, personalised recommendation explaining why these jobs "
        f"are suitable and what the worker should do next to apply."
    )

    prompt = build_rag_prompt(base_prompt, query, doc_type="job")
    return safe_generate(prompt, fallback_key="job_recommendation", max_tokens=300)
