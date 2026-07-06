"""Reject nonsense / hallucination-bait queries before search."""

import re
from typing import Tuple, List

IMPOSSIBLE_LOCATIONS = [
    "mars", "moon", "saturn", "jupiter", "venus", "pluto", "neptune",
    "andromeda", "atlantis", "narnia", "wakanda",
]

FAKE_BAIT_PATTERNS = [
    r"google\s+ceo\s+scholarship",
    r"elon\s+musk\s+scholarship",
    r"jeff\s+bezos\s+scholarship",
    r"scholarship\s+on\s+mars",
    r"scholarship\s+on\s+the\s+moon",
    r"100%\s+guaranteed\s+scholarship",
    r"instant\s+visa\s+scholarship",
]


def is_nonsense_query(query: str) -> Tuple[bool, str]:
    q = query.lower().strip()
    for loc in IMPOSSIBLE_LOCATIONS:
        if re.search(r"\b" + re.escape(loc) + r"\b", q):
            return True, f"No verified opportunities exist for locations like '{loc.title()}'."

    for pat in FAKE_BAIT_PATTERNS:
        if re.search(pat, q):
            return True, "No verified opportunities found for this query."

    return False, ""


def requires_high_confidence_match(query: str) -> bool:
    """Queries that must have strong dataset match or return empty."""
    q = query.lower()
    bait = ["ceo scholarship", "billionaire", "guaranteed", "100% free visa"]
    return any(b in q for b in bait)
