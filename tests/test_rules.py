from supportiq.priority import recommend_priority
from supportiq.routing import route_intent


def test_urgent_priority_is_explainable():
    priority, reasons = recommend_priority("I think my account was hacked")
    assert priority == "Urgent"
    assert "account hacked" in reasons


def test_default_priority_is_normal():
    priority, reasons = recommend_priority("How do I update my address?")
    assert priority == "Normal"
    assert reasons


def test_unknown_intent_routes_to_general_support():
    assert route_intent("unmapped_intent") == "General Banking Support"


def test_empty_intent_routes_to_general_support():
    assert route_intent("") == "General Banking Support"
