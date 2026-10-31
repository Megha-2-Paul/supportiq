from supportiq.priority import recommend_priority


def test_urgent_security_phrase_has_urgent_priority():
    priority, reasons = recommend_priority("My account was hacked yesterday")

    assert priority == "Urgent"
    assert "account hacked" in reasons


def test_high_priority_phrase_is_explained():
    priority, reasons = recommend_priority("My card is blocked")

    assert priority == "High"
    assert "card blocked" in reasons


def test_unmatched_message_defaults_to_normal():
    priority, reasons = recommend_priority("Where can I find my statement?")

    assert priority == "Normal"
    assert reasons == ["No configured urgency phrase matched"]
