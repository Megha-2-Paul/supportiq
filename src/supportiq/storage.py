"""SQLite prediction history; use synthetic or approved non-sensitive demo inputs."""
import sqlite3
from pathlib import Path
class TicketStore:
    def __init__(self, database_path: str = "supportiq.db"):
        self.database_path = database_path
        if database_path != ":memory:":
            Path(database_path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as con:
            con.execute("""CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, ticket_text TEXT NOT NULL,
                intent TEXT NOT NULL, confidence REAL NOT NULL, department TEXT NOT NULL,
                priority TEXT NOT NULL, sentiment TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
    def _connect(self):
        con = sqlite3.connect(self.database_path)
        con.row_factory = sqlite3.Row
        return con
    def add(self, text: str, result: dict) -> int:
        with self._connect() as con:
            cur = con.execute(
                "INSERT INTO predictions(ticket_text,intent,confidence,department,priority,sentiment) VALUES(?,?,?,?,?,?)",
                (text, result["intent"], result["confidence"], result["department"],
                 result["priority"], result["sentiment"]))
            return int(cur.lastrowid)
    def list_recent(self, limit: int = 100) -> list[dict]:
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")
        with self._connect() as con:
            rows = con.execute("SELECT * FROM predictions ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [dict(row) for row in rows]
