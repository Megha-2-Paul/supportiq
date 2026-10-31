import pytest
from pydantic import ValidationError
from supportiq.schemas import TicketRequest

def test_ticket_text_is_trimmed():
    assert TicketRequest(text="  Need help please ").text == "Need help please"

def test_whitespace_ticket_is_rejected():
    with pytest.raises(ValidationError):
        TicketRequest(text="   ")
