"""Explainable urgency heuristics; not a trained risk or priority model."""
import re
URGENT_TERMS = ("fraud", "stolen", "unauthorized", "account hacked", "scam", "security breach")
HIGH_TERMS = ("locked out", "cannot access", "payment failed", "card blocked", "money missing")
def recommend_priority(text: str) -> tuple[str, list[str]]:
    normalized = re.sub(r"\\s+", " ", text.lower())
    reasons = [term for term in URGENT_TERMS if term in normalized]
    if reasons:
        return "Urgent", reasons
    reasons = [term for term in HIGH_TERMS if term in normalized]
    if reasons:
        return "High", reasons
    return "Normal", ["No configured urgency phrase matched"]
