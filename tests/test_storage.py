import pytest
from supportiq.storage import TicketStore

def test_history_round_trip(tmp_path):
    store = TicketStore(str(tmp_path / "history.sqlite"))
    result = {"intent":"cash_withdrawal","confidence":0.9,"department":"Cash Services",
              "priority":"Normal","sentiment":"Not configured"}
    row_id = store.add("Cash was not dispensed", result)
    rows = store.list_recent()
    assert rows[0]["id"] == row_id
    assert rows[0]["intent"] == "cash_withdrawal"

def test_history_limit_validation(tmp_path):
    store = TicketStore(str(tmp_path / "history.sqlite"))
    with pytest.raises(ValueError):
        store.list_recent(0)
