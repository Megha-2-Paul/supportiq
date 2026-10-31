from supportiq.priority import recommend_priority
from supportiq.routing import route_intent


def test_urgent_priority_explains_match():
    level, reasons = recommend_priority("My account was hacked")
    assert level == "Urgent" and "account hacked" in reasons


def test_normal_priority_has_reason():
    level, reasons = recommend_priority("How can I change my address?")
    assert level == "Normal" and reasons


def test_unknown_route_goes_to_general_triage():
    assert route_intent("some_unmapped_intent") == "General Banking Support"
