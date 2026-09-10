"""
Simple RAG (Retrieval-Augmented Generation) engine.
Uses TF-IDF style cosine similarity for retrieval (no external vector DB required).
Augments prompts with relevant context chunks before calling IBM Granite.
"""

from __future__ import annotations

import math
import re
from typing import Any

from data.demo_data import (
    GOVERNMENT_SCHEMES,
    JOB_LISTINGS,
    TRAINING_PROGRAMMES,
    SKILL_TAXONOMY,
)


# ---------------------------------------------------------------------------
# Build a simple in-memory document store
# ---------------------------------------------------------------------------

def _build_corpus() -> list[dict[str, str]]:
    docs = []

    for j in JOB_LISTINGS:
        text = (
            f"Job: {j['title']}. Category: {j['category']}. "
            f"Description: {j['description']}. "
            f"Required skills: {', '.join(j['required_skills'])}. "
            f"Salary: ₹{j['salary_min']}–{j['salary_max']}/month. "
            f"Employer: {j['employer']}. Location: {j['location']}."
        )
        docs.append({"id": j["id"], "type": "job", "title": j["title"], "text": text})

    for t in TRAINING_PROGRAMMES:
        text = (
            f"Training: {t['name']}. Provider: {t['provider']}. "
            f"Skills covered: {', '.join(t['skills_covered'])}. "
            f"Duration: {t['duration']}. Cost: {t['cost']}. "
            f"Eligibility: {t['eligibility']}."
        )
        docs.append({"id": t["id"], "type": "training", "title": t["name"], "text": text})

    for s in GOVERNMENT_SCHEMES:
        text = (
            f"Scheme: {s['name']}. Category: {s['category']}. "
            f"Benefit: {s['benefit']}. "
            f"Eligibility: {s['eligibility']}. "
            f"Enroll at: {s['enroll_at']}."
        )
        docs.append({"id": s["id"], "type": "scheme", "title": s["name"], "text": text})

    # Add skill knowledge
    for category, skills in SKILL_TAXONOMY.items():
        text = f"Skill category: {category}. Skills include: {', '.join(skills)}."
        docs.append({"id": f"SK_{category}", "type": "skill", "title": category, "text": text})

    return docs


_CORPUS: list[dict[str, str]] = _build_corpus()


# ---------------------------------------------------------------------------
# Simple TF-IDF tokenizer + cosine similarity
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z₹0-9]+", text.lower())


def _term_freq(tokens: list[str]) -> dict[str, float]:
    tf: dict[str, float] = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1
    n = len(tokens) or 1
    return {k: v / n for k, v in tf.items()}


def _cosine_sim(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[k] * b[k] for k in common)
    mag_a = math.sqrt(sum(v * v for v in a.values()))
    mag_b = math.sqrt(sum(v * v for v in b.values()))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


# Pre-compute TF vectors for corpus
_CORPUS_TF: list[dict[str, float]] = [
    _term_freq(_tokenize(doc["text"])) for doc in _CORPUS
]


def retrieve(query: str, top_k: int = 4, doc_type: str | None = None) -> list[dict[str, Any]]:
    """
    Retrieve top-k most relevant documents for the query.
    Optionally filter by doc_type: 'job', 'training', 'scheme', 'skill'.
    """
    q_tf = _term_freq(_tokenize(query))
    scores = [
        (i, _cosine_sim(q_tf, corp_tf))
        for i, corp_tf in enumerate(_CORPUS_TF)
        if doc_type is None or _CORPUS[i]["type"] == doc_type
    ]
    scores.sort(key=lambda x: x[1], reverse=True)
    results = []
    for idx, score in scores[:top_k]:
        doc: dict[str, str | float] = dict(_CORPUS[idx])
        doc["score"] = round(score, 4)
        results.append(doc)
    return results


def build_rag_prompt(base_prompt: str, query: str, doc_type: str | None = None, top_k: int = 3) -> str:
    """
    Augment a prompt with retrieved context documents.
    """
    docs = retrieve(query, top_k=top_k, doc_type=doc_type)
    if not docs:
        return base_prompt

    context_lines = []
    for doc in docs:
        context_lines.append(f"[{doc['type'].upper()} – {doc['title']}]\n{doc['text']}")

    context_block = "\n\n".join(context_lines)
    return (
        f"Use the following reference information to answer accurately:\n\n"
        f"{context_block}\n\n"
        f"---\n\n"
        f"{base_prompt}"
    )
