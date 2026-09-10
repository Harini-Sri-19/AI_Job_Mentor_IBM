"""
Government Scheme Recommendation Agent.
Matches worker eligibility to government welfare schemes.
Uses IBM Granite for guidance narratives.
"""

from __future__ import annotations

from typing import Any

from data.demo_data import GOVERNMENT_SCHEMES
from rag_engine import build_rag_prompt
from watsonx_client import safe_generate

RATION_CARD_PRIORITY = {"AAY": 3, "BPL": 2, "PHH": 1, "APL": 0}


def _check_eligibility(worker: dict[str, Any], scheme: dict[str, Any]) -> tuple[bool, str]:
    """
    Heuristic eligibility check.
    Returns (is_eligible, reason_note).
    """
    elig = scheme.get("eligibility", "").lower()
    age = worker.get("age", 30)
    income = worker.get("monthly_income", 10000)
    name = scheme.get("name", "")

    # PM-SYM: age 18-40, income < 15000
    if "pm-sym" in name.lower() or "shram yogi" in name.lower():
        if 18 <= age <= 40 and income < 15000:
            return True, "Age and income criteria met"
        return False, f"Age must be 18–40 (yours: {age}) and income < ₹15,000"

    # ESIC: income < 21000
    if "esic" in name.lower():
        if income < 21000:
            return True, "Income within ESIC limit"
        return False, "Monthly income exceeds ₹21,000 ESIC limit"

    # BOCW: construction workers
    if "bocw" in name.lower() or "construction" in name.lower():
        occ = worker.get("current_occupation", "").lower()
        if "construct" in occ or "labour" in occ or "mason" in occ:
            return True, "Construction worker – eligible"
        return False, "Not a registered construction worker"

    # e-Shram: 16–59, informal worker
    if "e-shram" in name.lower() or "shram" in name.lower():
        if 16 <= age <= 59:
            return True, "Informal worker in eligible age range"
        return False, f"Age must be 16–59 (yours: {age})"

    # PMJDY: no bank account (but worker may already have one)
    if "jan dhan" in name.lower() or "pmjdy" in name.lower():
        if not worker.get("has_bank_account", True):
            return True, "No existing bank account – eligible"
        return True, "Can open additional Jan Dhan account for features"  # lenient

    # Sukanya: girl child
    if "sukanya" in name.lower():
        gender = worker.get("gender", "").lower()
        if gender == "female" and age <= 10:
            return False, "Sukanya is for girl children below 10 (enroll for your daughter)"
        return False, "Enroll for girl child below 10 years"

    # Generic check via income + age text
    eligible = True
    notes = []
    if "income" in elig and "15,000" in elig and income >= 15000:
        eligible = False
        notes.append("Income may exceed limit")
    if "18" in elig and age < 18:
        eligible = False
        notes.append("Age below minimum (18)")

    return eligible, "Likely eligible" if eligible else "; ".join(notes)


def get_scheme_recommendations(worker: dict[str, Any]) -> list[dict[str, Any]]:
    """Return schemes the worker is eligible for, with eligibility notes."""
    results = []
    for scheme in GOVERNMENT_SCHEMES:
        eligible, note = _check_eligibility(worker, scheme)
        priority = RATION_CARD_PRIORITY.get(worker.get("ration_card", "APL"), 0)
        results.append({
            **scheme,
            "is_eligible": eligible,
            "eligibility_note": note,
            "priority_score": priority + (2 if eligible else 0),
        })
    results.sort(key=lambda x: (x["is_eligible"], x["priority_score"]), reverse=True)
    return results


def get_scheme_narrative(
    worker: dict[str, Any],
    schemes: list[dict[str, Any]],
    language: str = "en",
) -> tuple[str, bool]:
    """Generate personalised scheme guidance using IBM Granite."""
    lang_inst = {
        "ta": "Respond in Tamil language.",
        "hi": "Respond in Hindi language.",
        "en": "Respond in English.",
    }.get(language, "Respond in English.")

    eligible_schemes = [s for s in schemes if s.get("is_eligible")]
    scheme_list = "\n".join(
        f"- {s['name']}: {s['benefit']} (enroll at: {s['enroll_at']})"
        for s in eligible_schemes[:4]
    )

    query = f"government welfare schemes informal worker {worker.get('current_occupation', '')} benefits"

    base_prompt = (
        f"{lang_inst}\n\n"
        f"You are a social welfare adviser for informal workers in India.\n"
        f"Worker: {worker.get('name')}, Age: {worker.get('age')}, "
        f"Income: ₹{worker.get('monthly_income')}/month, Occupation: {worker.get('current_occupation')}\n\n"
        f"Eligible government schemes:\n{scheme_list or 'None found'}\n\n"
        f"Write 3–4 sentences explaining the top 2 most important schemes this worker should enrol in immediately, "
        f"why they matter for financial security, and the first step to enrol."
    )

    prompt = build_rag_prompt(base_prompt, query, doc_type="scheme")
    return safe_generate(prompt, fallback_key="scheme", max_tokens=300)
