import pytest
from pydantic import ValidationError
from supportiq.schemas import TicketRequest


def test_ticket_text_is_trimmed():
    request = TicketRequest(text="  I need help  ")
    assert request.text == "I need help"


def test_ticket_rejects_whitespace():
    with pytest.raises(ValidationError):
        TicketRequest(text="   ")
