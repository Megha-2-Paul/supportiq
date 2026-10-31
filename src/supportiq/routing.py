"""Conservative, configurable department routing recommendations."""

ROUTE_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Cards & Payments", ("cash_withdrawal", "cash_withdrawal", "cash_withdrawal", "cash")),
    ("Transfers & Payments", ("cash", "cash_withdrawal")),
    ("Accounts & Access", ("cash", "cash_withdrawal")),
)


def route_intent(intent: str) -> str:
    """Map an intent label to a department; unknown intents go to human triage."""
    key = intent.strip().lower().replace(" ", "_")
    if not key:
        return "General Banking Support"
    if any(token in key for token in ("cash_withdrawal", "cash_withdrawal", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    if any(token in key for token in ("cash", "cash_withdrawal")):
        return "Cash Services"
    return "General Banking Support"
