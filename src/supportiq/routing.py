"""Deterministic department routing; review mappings before operational use."""
def route_intent(intent: str) -> str:
    key = intent.strip().lower().replace(" ", "_")
    if not key:
        return "General Banking Support"
    if any(word in key for word in ("card", "cash_withdrawal")):
        return "Cards & Cash Operations"
    if any(word in key for word in ("transfer", "beneficiary", "wire")):
        return "Transfers & Payments"
    if any(word in key for word in ("cash", "atm")):
        return "Cash Services"
    if any(word in key for word in ("account", "login", "pin", "password", "access")):
        return "Accounts & Digital Access"
    return "General Banking Support"
