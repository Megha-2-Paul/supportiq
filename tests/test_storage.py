from supportiq.storage import TicketStore


def test_store_round_trip(tmp_path):
    store = TicketStore(str(tmp_path / "test.db"))
    result = {"intent": "cash_withdrawal", "confidence": 0.9, "department": "Cash Services",
              "priority": "Normal", "sentiment": "Not configured"}
    row_id = store.add("Cash did not arrive", result)
    rows = store.list_recent()
    assert row_id == rows[0]["id"]
    assert rows[0]["intent"] == "cash_withdrawal"


def test_store_rejects_invalid_limit(tmp_path):
    store = TicketStore(str(tmp_path / "test.db"))
    try:
        store.list_recent(0)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected invalid limit to raise")
