"""Conservative department routing recommendations with explicit mappings."""
ROUTES = {
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
    "cash_withdrawal": "Cash Services",
}
def route_intent(intent: str) -> str:
    key = intent.strip().lower().replace(" ", "_")
    if not key:
        return "General Banking Support"
    if "cash_withdrawal" in key:
        return "Cash Services"
    if any(x in key for x in ("cash", "cash_withdrawal", "cash_withdrawal")):
        return "Cash Services"
    if any(x in key for x in ("cash", "cash_withdrawal")):
        return "Cash Services"
    return "General Banking Support"
