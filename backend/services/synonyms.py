"""Synonym and abbreviation normalization for search and matching."""

from typing import Dict, List, Set

# Maps abbreviations / aliases → canonical terms
FIELD_SYNONYMS: Dict[str, str] = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
    "nlp": "natural language processing",
    "cs": "computer science",
    "cse": "computer science",
    "it": "information technology",
    "ds": "data science",
    "ee": "electrical engineering",
    "ece": "electronics",
    "me": "mechanical engineering",
    "ce": "civil engineering",
    "mba": "business administration",
    "bio": "biology",
    "chem": "chemistry",
    "math": "mathematics",
    "stats": "statistics",
    "robotics": "robotics",
}

DEGREE_SYNONYMS: Dict[str, str] = {
    "ms": "masters",
    "msc": "masters",
    "m.sc": "masters",
    "m.sc.": "masters",
    "master of science": "masters",
    "master": "masters",
    "masters": "masters",
    "m.tech": "masters",
    "mtech": "masters",
    "mca": "masters",
    "mba": "mba",
    "bs": "bachelors",
    "bsc": "bachelors",
    "b.sc": "bachelors",
    "b.tech": "bachelors",
    "btech": "bachelors",
    "bachelor": "bachelors",
    "bachelors": "bachelors",
    "undergrad": "bachelors",
    "ug": "bachelors",
    "pg": "postgraduate",
    "phd": "phd",
    "doctorate": "phd",
    "postdoc": "postdoctoral",
    "diploma": "diploma",
}

COUNTRY_SYNONYMS: Dict[str, str] = {
    "us": "united states",
    "usa": "united states",
    "u.s.": "united states",
    "u.s.a.": "united states",
    "uk": "united kingdom",
    "u.k.": "united kingdom",
    "deutschland": "germany",
    "uae": "united arab emirates",
}

INTENT_PROVIDERS: Dict[str, List[str]] = {
    "germany": ["daad", "deutschlandstipendium", "erasmus"],
    "europe": ["erasmus", "daad", "fulbright"],
    "study_abroad": ["daad", "erasmus", "fulbright", "chevening"],
}

FIELD_EXPANSIONS: Dict[str, List[str]] = {
    "artificial intelligence": [
        "artificial intelligence", "machine learning", "computer vision",
        "robotics", "data science", "computer science", "deep learning",
    ],
    "machine learning": [
        "machine learning", "artificial intelligence", "data science",
        "computer science", "deep learning",
    ],
    "computer science": [
        "computer science", "artificial intelligence", "machine learning",
        "data science", "software engineering",
    ],
    "data science": [
        "data science", "machine learning", "artificial intelligence",
        "statistics", "analytics",
    ],
}


def normalize_term(term: str, synonym_map: Dict[str, str]) -> str:
    if not term:
        return ""
    key = term.lower().strip()
    return synonym_map.get(key, key)


def expand_field_terms(field: str) -> List[str]:
    """Expand a field of study into related search terms."""
    if not field:
        return []
    normalized = normalize_term(field, FIELD_SYNONYMS)
    for canonical, expansions in FIELD_EXPANSIONS.items():
        if normalized in canonical or canonical in normalized:
            return list(dict.fromkeys(expansions))
    return [normalized, field.lower()]


def expand_query_terms(text: str) -> Set[str]:
    """Tokenize and expand a query with synonyms."""
    if not text:
        return set()
    terms: Set[str] = set()
    lower = text.lower()
    terms.add(lower)

    for abbr, canonical in {**FIELD_SYNONYMS, **DEGREE_SYNONYMS, **COUNTRY_SYNONYMS}.items():
        if abbr in lower.split() or f" {abbr} " in f" {lower} " or lower.startswith(abbr + " ") or lower.endswith(" " + abbr):
            terms.add(canonical)
            terms.add(abbr)

    for word in lower.split():
        if word in FIELD_SYNONYMS:
            terms.add(FIELD_SYNONYMS[word])
        if word in DEGREE_SYNONYMS:
            terms.add(DEGREE_SYNONYMS[word])
        if word in COUNTRY_SYNONYMS:
            terms.add(COUNTRY_SYNONYMS[word])

    return terms
