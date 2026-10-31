"""ASGI entry point: uvicorn api.main:app --reload."""
from supportiq.api import app

__all__ = ["app"]
